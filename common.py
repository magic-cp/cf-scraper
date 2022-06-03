"""
Utilities to scrap the problem details of a codeforces problem.

Date created: 2022-05-16
Date of when codeforces was studied for scraping: 2022-05-16
"""
import json
import csv
import os
import argparse
from dataclasses import dataclass
from typing import List

import cf_api

CF_PROBLEMS = 'input/problems.json'
CF_CONTESTS = 'input/contests.json'

@dataclass
class Contest:
    """
    Small representation of a contest from CF API
    """
    name: str
    phase: str
    contest_id: int

@dataclass
class Problem:
    """
    Small representation of a problem from CF API
    """
    index: str
    contest_id: int
    name: str
    tags: List[str]
    solved_count: int = 0

    def get_url(self):
        return f'https://codeforces.com/contest/{self.contest_id}/problem/{self.index}'

    def __str__(self) -> str:
        return f'{self.contest_id}{self.index} - {self.name}'

def map_to_contest(cf_response):
    return [Contest(contest['name'], contest['phase'], contest['id']) for contest in cf_response['result']]

def map_to_problem(cf_response):
    problems = [Problem(problem['index'], problem['contestId'], problem['name'], problem['tags']) for problem in cf_response['result']['problems']]

    problem_to_solved_count = {}
    for stat in cf_response['result']['problemStatistics']:
        problem_to_solved_count[(stat['contestId'], stat['index'])] = stat['solvedCount']

    for problem in problems:
        problem.solved_count = problem_to_solved_count.get((problem.contest_id, problem.index), 0)
    return problems


def load_and_store_response(file_name, mapper):
    def dec(func):
        def wrapped(*args, **kwargs):
            force_reload = kwargs['force_reload'] if 'force_reload' in kwargs else False
            if not force_reload and os.path.exists(file_name):
                with open(file_name, 'r') as f:
                    return mapper(json.load(f))

            problems_json = func()


            with open(file_name, 'w') as f:
                json.dump(problems_json, f, indent=2)

            return mapper(problems_json)
        return wrapped
    return dec

@load_and_store_response(CF_PROBLEMS, map_to_problem)
def load_problems() -> List[Problem]:
    return cf_api.get_problems()

@load_and_store_response(CF_CONTESTS, map_to_contest)
def load_contests() -> List[Contest]:
    return cf_api.get_contests()

def default_argument_parser():
    args = argparse.ArgumentParser(description='Utility to scrap information from Codeforces')

    args.add_argument('--force-download-of-problems', help='Self explanatory', action='store_true')
    args.add_argument('--force-download-of-contests', help='Self explanatory', action='store_true')
    return args

def parse_args():
    return default_argument_parser().parse_args()

def main():
    args = parse_args()
    print('Loading problems from CF...')
    problems = load_problems(force_reload=args.force_download_of_problems)
    print('✅ Done')
    print('Loading contests from CF...')
    contests = load_contests(force_reload=args.force_download_of_contests)
    print('✅ Done')

    # educational_contests = [contest for contest in contests if contest.name.startswith('Educational') and contest.phase == 'FINISHED']
    # print(f'Found {len(educational_contests)} educational contests')
    # print('First 10 educational contests:')
    # pprint.pprint(educational_contests[:10])

    print()
    # print('\n\n')
    # print('Contests found in first 10 of the list:')
    # first_10_edu_contests = educational_contests[:10]

    # problems_in_first_10_contests = [problem for contest in first_10_edu_contests for problem in problems if problem.contest_id == contest.contest_id and problem.index in 'AB']
    # print(f'Found {len(problems_in_first_10_contests)} problems in first 10 educational contests')
    # problems_in_first_10_contests_grouped = groupby(problems_in_first_10_contests, lambda problem: problem.contest_id)
    # for contest_id, problems in problems_in_first_10_contests_grouped:
    #     print('Contest id:', contest_id)
    #     for problem in problems:
    #         print(f'* {problem.name} - {problem.get_url()}')
    #     print()


if __name__ == '__main__':
    main()
    # pprinter = pprint.PrettyPrinter()
    # pprinter.pprint(get_problem_details(282, 'A'))
