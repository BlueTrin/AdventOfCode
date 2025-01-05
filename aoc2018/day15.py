import os

import colorama
from aoc_lube import fetch, submit
from utils2018 import aoc_timer, parse_complex
from typing import Dict, List, Tuple, Set
import math
import copy
import itertools
import networkx as nx
import scipy
import numpy as np
from dataclasses import dataclass
from collections import deque , defaultdict
import enum
from heapq import heappush, heappop
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
import keyboard
import time
# GCD -> math.gcd

# all combinations (no order):
# >>> list(itertools.combinations([1,2,3], 2))
# [(1, 2), (1, 3), (2, 3)]

# all permutations
# >>> list(itertools.permutations([1,2,3], 2))
# [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]

# product
# >>> list(itertools.product([1,2,3], repeat=2))
# [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]

# GENERAL DEFINITIONS # GENERAL DEFINITIONS # GENERAL DEFINITIONS # GENERAL DEFINITIONS # GENERAL DEFINITIONS # GENERAL DEFINITIONS

N = -1j
S = 1j
W = -1
E = 1

ALLDIRS = [N, S, E, W]

NW = N + W
NE = N + E
SW = S + W
SE = S + E

def print_maze(nodes, coords, anti ):
	s = ""
	for y in range(int(coords.imag)):
		for x in range(int(coords.real)):
			pt = x + y * 1j
			if pt in anti:
				s += "#"
			else:
				is_node = False
				for c, node_pts in nodes.items():
					if pt in node_pts:
						s += c
						is_node = True
						break
				if not is_node:
					s += "."

		s += "\n"
	print(s)


i1 = '''#######   
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#   
####### 
'''
 #  CODE HERE  #  CODE HERE  #  CODE HERE  #  CODE HERE  #  CODE HERE  #  CODE HERE  #  CODE HERE  #  CODE HERE  #  CODE HERE

class Team(enum.Enum):
	ELF = enum.auto()
	GOBLIN = enum.auto()

UNITID: int = 0

@dataclass
class Unit:
	team: Team
	pos: complex
	hp: int = 200
	atk: int = 3
	def __post_init__(self):
		global UNITID
		self.id = UNITID
		UNITID += 1

class OMGElfDied(Exception):
	def __init__(self, message):
		# Call the base class constructor with the parameters it needs
		super().__init__(message)

class NoEnemiesLeft(Exception):
	def __init__(self, message):
		# Call the base class constructor with the parameters it needs
		super().__init__(message)

def find_shortest_path_heapq(start, walls, targets, min_shortest=math.inf):
	entry_count = 0
	q = []
	res = None
	seen_len = {}

	def dst_to_unit(p1, p2):
		return abs(p1.real - p2.real) + abs(p1.imag - p2.imag)

	heappush(q, (
		min([dst_to_unit(start, t) for t in targets]),
		0,
		entry_count,
		start, [start]))
	entry_count += 1
	while q:
		_dst_to_enemy, depth, _, pos, path = heappop(q)
		if seen_len.get(pos, math.inf) <= depth or depth >= min_shortest:
			continue
		seen_len[pos] = depth

		if pos in walls:
			continue
		for d in ALLDIRS:
			if pos+d in targets:
				min_shortest = min(min_shortest, depth)
				if res is None:
					res = path[1:]+[pos+d]
				elif len(path[1:]+[pos+d]) < len(res):
					res = path[1:]+[pos+d]
				continue
			if pos + d not in walls:
				if pos+d in path or seen_len.get(pos+d, math.inf) <= depth+1:
					continue
				dst_to_enemy = min([dst_to_unit(pos+d, w) for w in walls])
				if min_shortest <= depth+1 + dst_to_enemy:
					continue
				heappush(q, (
					dst_to_enemy,
					depth+1,
					entry_count,
					pos+d, path + [pos+d])
				)
				entry_count += 1
	return res

def bfs(start, walls, goals):
	# traverse the cave in distance/reading order
	visited = set()
	check = deque([[start]])
	visited.add(start)
	while len(check):
		path = check.popleft()
		c = path[-1] # most recent coord

		if c in goals:
			return path[1:] # next move is the first step in this path
		for d in [N, W, E, S]: # Reading order!
			if c+d not in walls and not c+d in visited:
				visited.add(c+d)
				check.append(path+[c+d])
	return [] # no path to any goals

def print_2dgrid(c_to_cos, cos_highlight):
	min_x = int(min(co.real for cos in c_to_cos.values() for co in cos))
	min_y = int(min(co.imag for cos in c_to_cos.values() for co in cos))
	max_x = int(max(co.real for cos in c_to_cos.values() for co in cos))
	max_y = int(max(co.imag for cos in c_to_cos.values() for co in cos))
	s = ""
	for y in range(min_y, max_y+1):
		for x in range(min_x, max_x+1):
			c_to_add = " "
			for c, cos in c_to_cos.items():
				if x + y * 1j in cos:
					c_to_add = c
					break
			if x + y * 1j in cos_highlight:
				s += colorama.Back.YELLOW
				s += c_to_add
				s += colorama.Back.BLACK
			else:
				s += c_to_add
		s += "\n"
	print(s)

@dataclass
class Game:
	units: List[Unit]
	walls: Set[complex]
	dims: Tuple[int, int]
	rounds: int = 0
	dead: List[Unit] = None

	def print_maze(self):
		s = f" ** Rounds: {self.rounds} ** \n" + self.format_maze()
		logger.info(s)

	def format_maze(self):
		s = ""
		for y in range(self.dims[1]):
			hp_legend = ""
			for x in range(self.dims[0]):
				pt = x + y * 1j
				if pt in self.walls:
					s += "#"
				else:
					is_unit = False
					for u in self.units:
						if u.pos == pt:
							s += "G" if u.team == Team.GOBLIN else "E"
							hp_legend += f"{u.team.name[0]}({u.hp}), "
							is_unit = True
							break
					if not is_unit:
						s += " "
			# add hp
			s += " " + hp_legend
			s += "\n"
		return s

	def __post_init__(self):
		if self.dead is None:
			self.dead = []

	def sort_key(self, c):
		return c.imag * self.dims[0] + c.real

	def enemies_in_range(self, unit):
		res = []
		for other in self.units:
			if other.team != unit.team and (other.pos - unit.pos) in ALLDIRS:
				res.append(other)
		res.sort(key=lambda u: (u.hp, self.sort_key(u.pos)))
		return res

	def move(self, unit):
		enemies = [u for u in self.units if u.team != unit.team]
		if not enemies:
			raise NoEnemiesLeft("No enemies left")
		if enemies_in_range := self.enemies_in_range(unit):
			# unit in range of enemy
			logger.debug(f"{unit.team} at {unit.pos} in range of {enemies_in_range[0].team} at {enemies_in_range[0].pos}")
			return

		# enemies_path = bfs(unit.pos, self.walls | {enemy.pos for enemy in self.units if enemy.team == unit.team}, {enemy.pos for enemy in self.units if enemy.team != unit.team})
		enemies_path = self.find_all_path_heapq(unit)
		# if enemies_path:
		# 	print_2dgrid({'#': self.walls} | {'E': {unit.pos for unit in self.units if unit.team == Team.ELF}} | {
		# 		'G': {unit.pos for unit in self.units if unit.team == Team.GOBLIN}}, set(enemies_path))
		# 	assert enemies_path[0] == enemies_paths2[0]
		if not enemies_path:
			logger.debug(f"no enemies found unit={unit.pos}")
		else:
			logger.debug(f"{unit.team} at {unit.pos} move to {enemies_path[0]}")
			assert unit.pos != enemies_path[0]
			assert enemies_path[0] not in {other.pos for other in self.units}
			unit.pos = enemies_path[0]

	def can_reach_enemy(self, unit, max_len=math.inf):
		enemies_pos = {u.pos for u in self.units if u.team != unit.team}
		allies_pos = {u.pos for u in self.units if u.team == unit.team}

		fill = set()
		fill.add(unit.pos)

		has_filled = True
		dist = 0
		while has_filled:
			has_filled = False
			added_points = set()
			dist += 1
			if dist > max_len:
				return False
			for pt in fill:
				for d in ALLDIRS:
					if pt + d not in fill and pt + d not in self.walls and pt + d not in allies_pos:
						if pt+d in enemies_pos:
							return dist
						added_points.add(pt + d)
						has_filled = True
			fill |= added_points
		return False

	def find_path_dumbass(self, unit, min_shortest=math.inf):
		res = []
		enemies_pos = {u.pos for u in self.units if u.team != unit.team}
		walls = self.walls | {u.pos for u in self.units if u.team == unit.team}
		seen = {}
		for d in ALLDIRS:
			if unit.pos+d not in walls:
				sol = find_shortest_path_heapq(unit.pos+d, walls, enemies_pos, min_shortest=len(res) if res else math.inf)
				assert unit.pos != sol[0] if sol else True
				if sol:
					res.append([unit.pos+d] +sol)
		res.sort(key=lambda x: (len(x), self.sort_key(x[0])))
		return res[0] if res else None

	def find_all_path_heapq(self, unit, min_shortest=math.inf):
		res = []
		entry_count = 0
		q = []
		target_pos = {u.pos for u in self.units if u.team != unit.team}
		walls = self.walls | {u.pos for u in self.units if u.team == unit.team}
		seen_len = defaultdict(dict)   # we need to store len with the first node
		heappush(q, (
			0,
			entry_count,
			unit.pos, []))
		entry_count += 1
		while q:
			depth, _, pos, path = heappop(q)
			if path and seen_len.get(path[0], {}).get(path[-1], math.inf) <= depth:
				continue
			if depth > min_shortest:
				continue
			if path:
				if path[0] not in seen_len:
					seen_len[path[0]] = {}
				if path[-1] not in seen_len[path[0]]:
					seen_len[path[0]][path[-1]] = depth
				else:
					seen_len[path[0]][path[-1]] = min(seen_len[path[0]][path[-1]], depth)
			if pos in target_pos:
				res.append(path)
				min_shortest = min(min_shortest, depth)
			for d in ALLDIRS:
				if pos+d in walls:
					continue
				heappush(q, (
					depth+1,
					entry_count,
					pos+d, path+[pos+d]))
				entry_count+=1
		res.sort(key=lambda x: (len(x), self.sort_key(x[-1]), self.sort_key(x[0])))
		return res[0] if res else None


	def find_all_path_heapq_old(self, unit, min_shortest=math.inf):
		entry_count = 0
		q = []
		enemies_pos = {u.pos for u in self.units if u.team != unit.team}
		walls = {u.pos for u in self.units if u.team == unit.team and u is not unit}

		res = {min_shortest: []}
		seen_len = {}
		def dst_to_unit(p1, p2):
			return abs(p1.real - p2.real) + abs(p1.imag - p2.imag)

		heappush(q, (
			min([dst_to_unit(unit.pos, epos) for epos in enemies_pos]),
			0,
			entry_count,
			unit.pos, [unit.pos]))
		entry_count += 1
		while q:
			_dst_to_enemy, depth, _, pos, path = heappop(q)
			if seen_len.get(pos, math.inf) < depth or depth > min_shortest:
				continue
			seen_len[pos] = depth

			if pos in enemies_pos:
				if depth not in res:
					res[depth] = []
				min_shortest = min(min_shortest, depth)
				res[depth].append((pos, path[1:]+[pos]))
				continue
			for d in ALLDIRS:
				if pos + d not in self.walls and pos+d not in {u.pos for u in self.units if u.team == unit.team}:
					if pos+d in path or seen_len.get(pos+d, math.inf) < depth+1:
						continue
					dst_to_enemy = min([dst_to_unit(pos+d, epos) for epos in enemies_pos])
					if min_shortest < depth+1 + dst_to_enemy:
						continue
					heappush(q, (
						dst_to_enemy,
						depth+1,
						entry_count,
						pos+d, path + [pos+d])
					)
					entry_count += 1
		return res[min_shortest]

	def find_path_deque(self, unit, pos):
		'''
		Returns all of the shortest paths to the nearest enemy as a list of tuples:
			- (enemy pos, path)
		'''
		q = deque([(pos, [unit.pos], 0)])
		min_shortest = math.inf
		res = {min_shortest: []}
		seen_len = {}
		while q:
			pos, path, depth = q.popleft()
			if pos not in seen_len or seen_len[pos] > len(path):
				seen_len[pos] = depth

			if len(path) >= min_shortest:
				continue

			for d in ALLDIRS:
				if pos + d not in self.walls and pos+d not in {u.pos for u in self.units if u.team == unit.team}:
					if pos+d in path:
						continue

					if pos+d in {u.pos for u in self.units if u.team != unit.team}:
						if len(path)+1 not in res:
							res[len(path)+1] = []
						res[len(path)+1].append((pos+d, path[1:] + [pos+d]))
						min_shortest = min(min_shortest, len(path)+1)
					else:
						if seen_len.get(pos+d, math.inf) >= depth+1:
							q.append((pos+d, path + [pos+d], depth+1))
		return res[min_shortest]

	def round(self, throw_elfdied=False):
		self.units.sort(key=lambda u: u.pos.imag * self.dims[0] + u.pos.real)
		unit_order = copy.copy(self.units)
		for unit in unit_order:
			if unit.hp <= 0:
				continue
			self.move(unit)
			self.attack(unit, throw_elfdied=throw_elfdied)

		self.rounds += 1
		if logger.level <= logging.DEBUG:
			self.print_maze()
		return True

	def attack(self, unit, throw_elfdied):
		"""
		To attack, the unit first determines all of the targets that are in range of it by being immediately adjacent to
		it. If there are no such targets, the unit ends its turn. Otherwise, the adjacent target with the fewest hit points
		is selected; in a tie, the adjacent target with the fewest hit points which is first in reading order is selected.

		The unit deals damage equal to its attack power to the selected target, reducing its hit points by that amount. If this
		reduces its hit points to 0 or fewer, the selected target dies: its square becomes . and it takes no further turns.
		"""
		enemies = [u for u in self.units if u.team != unit.team]
		if not enemies:
			raise NoEnemiesLeft("No enemies left")

		if enemies := self.enemies_in_range(unit):
			enemies[0].hp -= unit.atk
			logger.debug(f"{unit.team} at {unit.pos} attacks {enemies[0].team} at {enemies[0].pos} {enemies[0].hp} hp left")
			if enemies[0].hp <= 0:
				if enemies[0].team == Team.ELF and throw_elfdied:
					raise OMGElfDied("Elf died")

				self.dead.append(enemies[0])
				self.units.remove(enemies[0])
				logger.debug(f"{enemies[0].team} at {enemies[0].pos} died")


def read_grid(inp, elf_atk):
	total = 0
	co_to_c, c_to_co, dims = parse_complex(inp)
	g = Game([], set(), dims)
	for c in c_to_co['#']:
		g.walls.add(c)
	for c in c_to_co['G']:
		g.units.append(Unit(Team.GOBLIN, c))
	for c in c_to_co['E']:
		g.units.append(Unit(Team.ELF, c, atk=elf_atk))
	return g

def part1(inp, debug=False, interactive=False, get_history=False):
	g = read_grid(inp ,elf_atk=3)
	game_states = {}
	try:
		while True:
			if interactive or get_history:
				game_states[g.rounds] = copy.deepcopy(g)
			if g.rounds % 5 == 0:
				logger.info(f"Round {g.rounds} Goblin HP{sum(u.hp for u in g.units if u.team == Team.GOBLIN)} ELF HP {sum(u.hp for u in g.units if u.team == Team.ELF)}")
			if not g.round():
				break
	except NoEnemiesLeft:
		pass

	remaining_hp = sum(u.hp for u in g.units)
	total = g.rounds * remaining_hp

	history = {}
	if get_history:
		for i, gs in game_states.items():
			history[i] = g.format_maze()

	if interactive:
		for i, gs in game_states.items():
			g.print_maze()
			input("Press Enter to continue...")

	if history:
		return total, history
	else:
		return total

def part2(inp):
	elf_atk = 4
	while True:
		logger.info(f"Trying elf attack power: {elf_atk}")
		g = read_grid(inp ,elf_atk=elf_atk)
		try:
			while True:
				g.round(throw_elfdied=True)
		except OMGElfDied:
			elf_atk += 1
			continue
		except NoEnemiesLeft:
			break
	print(f"Elf attack power: {elf_atk}")
	remaining_hp = sum(u.hp for u in g.units)
	total = g.rounds * remaining_hp
	return total

# RUN STUFF HERE # RUN STUFF HERE # RUN STUFF HERE # RUN STUFF HERE # RUN STUFF HERE # RUN STUFF HERE # RUN STUFF HERE # RUN STUFF HERE
#
if __name__ == '__main__':
	sol1 = part1(i1)
	print(sol1)
	assert sol1 == 27730

	i2 = '''#######
	#G..#E#
	#E#E.E#
	#G.##.#
	#...#E#
	#...E.#
	#######'''
	sol1 = part1(i2, debug=True)
	print(sol1)
	assert sol1 == 36334
	i3 = '''#######   
	#E..EG#
	#.#G.E#
	#E.##E#
	#G..#.#
	#..E#.#   
	#######   
	'''
	sol1 = part1(i3)
	print(sol1)
	assert sol1 == 39514

	i4 = '''#######
	#E.G#.#
	#.#G..#
	#G.#.G#
	#G..#.#
	#...E.#
	#######
	'''
	sol1 = part1(i4)
	print(sol1)
	assert sol1 == 27755

	i5 = '''#######
	#.E...#
	#.#..G#
	#.###.#
	#E#G#G#
	#...#G#
	#######
	'''
	sol1 = part1(i5, interactive=False)
	print(sol1)
	assert sol1 == 28944

	i6 = '''#########
	#G......#
	#.E.#...#
	#..##..G#
	#...##..#
	#...#...#
	#.G...G.#
	#.....G.#
	#########
	'''
	sol1 = part1(i6)
	print(sol1)
	assert sol1 == 18740

	ii = fetch(2018, 15)
	logger.setLevel(logging.INFO)
	sol1, history = part1(ii, get_history=True)
	print(sol1)


	sol2 = part2(i1)
	print(sol2)
	# print_maze(nodes, coords, anti)

	sol2 = part2(ii)
	print(sol2)
