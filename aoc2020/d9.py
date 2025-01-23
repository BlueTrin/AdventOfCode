from aoc_lube import fetch

s = fetch(2020, 9)

nums = list(map(int, s.splitlines()))

for i in range(25, len(nums)):
    if not any(nums[j] + nums[k] == nums[i] for j in range(i-25, i) for k in range(j, i)):
        invalid = nums[i]
        break

print(f"Part1: {invalid}")

for i in range(len(nums)):
    for j in range(i+2, len(nums)):
        if sum(nums[i:j]) == invalid:
            break
    else:
        continue

    break


print(f"Part2: {min(nums[i:j]) + max(nums[i:j])}")
