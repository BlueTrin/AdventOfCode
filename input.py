import sys
from os import path, makedirs, getenv
from tempfile import gettempdir
from urllib import request

from adventofcode import parse_args

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

    session_token = "_ga=GA1.2.936012548.1702496502; _ga_MHSNPJKWC7=GS1.2.1724569495.74.0.1724569495.0.0.0; session=53616c7465645f5f234ee02a1ebb481d7dd4140babd4ba3101cecf4ba638038c751b14f000ae74da52ac5938838f674c3454ad358ab958fd5a783dd37faf0aa2"
    #session_token = args.session or getenv('AOC_SESSION_ID')
    if not session_token:
        sys.exit("set AOC_SESSION_ID environment variable or specify -s argument")
    input_url = f'https://adventofcode.com/{year}/day/{day}/input'
    input_request = request.Request(
        input_url, headers={'Cookie': f'session={session_token}'}
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
