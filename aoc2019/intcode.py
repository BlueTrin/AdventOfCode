# Description: Intcode computer for Advent of Code 2019
from collections import defaultdict, deque
import copy

class Arg(object):
    def __init__(self, mode, value, p, relative_base):
        self.mode = mode
        self.value = value
        self.p = p
        self.relative_base = relative_base


    def __repr__(self):
        return f'{self.mode}:{self.value}'

    def get(self):
        # For example, given a relative base of 50, a relative mode parameter of -7 refers to memory address 50 + -7 = 43.
        if self.mode == 0:
            return self.p[self.value]
        elif self.mode == 1:
            return self.value
        elif self.mode == 2:
            return self.p[self.value + self.relative_base]
        else:
            raise Exception(f'Unknown mode {self.mode}')

    def set(self, value):
        if self.mode == 0:
            self.p[self.value] = value
        elif self.mode == 1:
            raise Exception('Immediate mode is not settable')
        elif self.mode == 2:
            self.p[self.value + self.relative_base] = value
        else:
            raise Exception(f'Unknown mode {self.mode}')

class Intcode(object):
    def __init__(self, program):
        self.p = defaultdict(int, {i: v for i, v in enumerate(program)})
        self.orig_p = copy.deepcopy(self.p)
        self.ptr = 0
        self.output = deque()
        self.input = []
        self.halted = False
        self.relative_base = 0
        self.input_needed = False
        self.network_mode = False

    def reset(self):
        self.p = copy.deepcopy(self.orig_p)
        self.ptr = 0
        self.output = deque()
        self.input = []
        self.halted = False
        self.relative_base = 0
        self.input_needed = False

    def add_input(self, value):
        self.input.append(value)

    def run(self, stop_at_output=False):
        while self.p[self.ptr] != 99 and not self.halted:
            instr, a, b, c = (self.p.get(self.ptr + i, 0) for i in range(4))
            opcode = instr % 100
            mode1 = (instr // 100) % 10
            mode2 = (instr // 1000) % 10
            mode3 = (instr // 10000) % 10

            a1, a2, a3 = (Arg(mode1, a, self.p, self.relative_base),
                          Arg(mode2, b, self.p, self.relative_base),
                          Arg(mode3, c, self.p, self.relative_base))

            if opcode == 1:
                self.opcode1(a1, a2, a3)
                self.ptr += 4
            elif opcode == 2:
                self.opcode2(a1, a2, a3)
                self.ptr += 4
            elif opcode == 3:
                if not self.input:
                    if self.network_mode:
                        self.input.append(-1)
                    else:
                        self.input_needed = True
                        return
                self.input_needed = False
                self.opcode3(a1)
                self.ptr += 2
            elif opcode == 4:
                self.opcode4(a1)
                self.ptr += 2
                if stop_at_output:
                    return
            elif opcode == 5:
                self.opcode5(a1, a2)
            elif opcode == 6:
                self.opcode6(a1, a2)
            elif opcode == 7:
                self.opcode7(a1, a2, a3)
                self.ptr += 4
            elif opcode == 8:
                self.opcode8(a1, a2, a3)
                self.ptr += 4
            elif opcode == 9:
                self.opcode9(a1)
                self.ptr += 2
            else:
                raise RuntimeError(f'Unknown opcode {opcode} at {self.ptr}')
        self.halted = True

    def opcode1(self, a, b, c):
        '''
        Opcode 1 adds together numbers read from two positions and stores the result in a third position.
        The three integers immediately after the opcode tell you these three positions -
         the first two indicate the positions from which you should read the input values, and the
         third indicates the position at which the output should be stored.
        '''
        c.set(a.get() + b.get())
        return self.p

    def opcode2(self, a, b, c):
        '''
        Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them.
        Again, the three integers after the opcode indicate where the inputs and outputs are, not their values.
        '''
        c.set(a.get() * b.get())
        return self.p

    def opcode3(self, a):
        '''
        Opcode 3 takes a single integer as input and saves it to the position given by its only parameter.
        For example, the instruction 3,50 would take an input value and store it at address 50.
        '''
        if self.input:
            a.set(self.input.pop(0))
        else:
            raise RuntimeError('No input')
        return self.p

    def opcode4(self, a):
        '''
        Opcode 4 outputs the value of its only parameter.
        For example, the instruction 4,50 would output the value at address 50.
        '''
#        print(a.get())
        self.output.append(a.get())
        return self.p

    def opcode5(self, a, b):
        '''
        Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value
        from the second parameter. Otherwise, it does nothing.
        '''
        if a.get() != 0:
            self.ptr = b.get()
        else:
            self.ptr += 3
        return self.p

    def opcode6(self, a, b):
        '''
        Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value
        from the second parameter. Otherwise, it does nothing.
        '''
        if a.get() == 0:
            self.ptr = b.get()
        else:
            self.ptr += 3
        return self.p

    def opcode7(self, a, b, c):
        '''
        Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position
        given by the third parameter. Otherwise, it stores 0.
        '''
        c.set(1 if a.get() < b.get() else 0)
        return self.p

    def opcode8(self, a, b, c):
        '''
        Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position
        given by the third parameter. Otherwise, it stores 0.
        '''
        c.set(1 if a.get() == b.get() else 0)
        return self.p

    def opcode9(self, a):
        '''
        Opcode 9 adjusts the relative base by the value of its only parameter.
        The relative base increases (or decreases, if the value is negative) by the value of the parameter.
        '''
        self.relative_base += a.get()
        return self.p