import sys
from os import path, makedirs, getenv
from tempfile import gettempdir
from urllib import request

import argparse

# see https://github.com/wimglenn/advent-of-code-wim/issues/1
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('day', default=0, type=int, nargs='?',
                        help='challenge calendar day, 0 solves all')
    parser.add_argument('-p', '--part', dest='part', default=0, type=int, choices=range(3),
                        help='solve task part 1 or 2, 0 solves both')
    parser.add_argument('-y', '--year', dest='year', default=2022, type=int, choices=range(2015, 2022),
                        help='solve tasks from this year')
    parser.add_argument('-c', '--cache', dest='cache_dir',
                        help='directory where to store challenge input strings')
    parser.add_argument('-s', '--session', dest='session',
                        help='adventofcode.com login session cookie')
    return parser.parse_args()


# see https://github.com/wimglenn/advent-of-code-wim/issues/1
def get_input(day: int, year: int = 2020):
    args = parse_args()
    input_dir = args.cache_dir or path.join(gettempdir(), 'aoc_cache')
    input_dir = path.join(input_dir, str(year))
    input_path = path.join(input_dir, str(day) + '.txt')
    if path.isfile(input_path):
        print(f'loading {input_path}')
        with open(input_path, 'r') as f:
            return f.read()

    import session_token
    aoc_session_id = session_token.aoc_session_id or getenv('AOC_SESSION_ID')
    if not aoc_session_id:
        sys.exit("set AOC_SESSION_ID environment variable or specify -s argument")
    input_url = f'https://adventofcode.com/{year}/day/{day}/input'
    input_request = request.Request(
        input_url, headers={'Cookie': f'session={aoc_session_id}'}
    )
    print(f'fetching input data from {input_url}')
    with request.urlopen(input_request) as response:
        input_str = response.read()
        if not path.isdir(input_dir):
            makedirs(input_dir)
        with open(input_path, 'wb') as f:
            f.write(input_str)
            print(f'saved downloaded input to {input_path}')
        return input_str.decode()
