"""
Utilities to scrap the problem details of a codeforces problem.

Date created: 2022-05-16
Date of when codeforces was studied for scraping: 2022-05-16
"""
import json
import requests
import pprint
import csv
import os
import argparse
from dataclasses import dataclass

import cf_api
from bs4 import BeautifulSoup

PROBLEM_STATEMENT_SELECTOR = '.problem-statement'
TITLE_SELECTOR = ".title"
STATEMENT_SELECTOR = '.header + div'
INPUT_SPECIFICATION_SELECTOR = '.input-specification'
OUTPUT_SPECIFICATION_SELECTOR = '.output-specification'

DATASET_FILE = os.path.join('dataset', 'cf_problems.csv')
INPUT_FILE = os.path.join('dataset', 'input.csv')

CONTEST_ID = 'contest_id'
PROBLEM_ID = 'problem_id'
TITLE = 'title'
STATEMENT = 'statement'
INPUT_SPEC = 'input_spec'
OUTPUT_SPEC = 'output_spec'

CF_PROBLEMS = 'input/problems.json'
CF_CONTESTS = 'input/contests.json'

def get_csv_reader(file_name):
    with open(file_name, 'w+') as csv_file:
        return csv.DictReader(csv_file)

def get_csv_writer(file_name):
    with open(file_name, 'w+') as csv_file:
        return csv.DictWriter(csv_file, fieldnames=[CONTEST_ID, PROBLEM_ID, TITLE, STATEMENT, INPUT_SPEC, OUTPUT_SPEC])

def get_problem_title(soup: BeautifulSoup):
    # we splice because the problem title has the problem id in it e.g. "A. Bit++"
    return soup.select_one(TITLE_SELECTOR).text[3:]

def get_problem_statement(soup: BeautifulSoup):
    return soup.select_one(STATEMENT_SELECTOR).text

def get_input_spec(soup: BeautifulSoup):
    return soup.select_one(INPUT_SPECIFICATION_SELECTOR).text

def get_output_spec(soup: BeautifulSoup):
    return soup.select_one(OUTPUT_SPECIFICATION_SELECTOR).text

def get_problem_details(contest_id, problem_id):

    URL = f"https://codeforces.com/contest/{contest_id}/problem/${problem_id}"

    page = requests.get(URL)


    soup = BeautifulSoup(page.content, "html.parser").select_one(PROBLEM_STATEMENT_SELECTOR)

    # print(soup)
    return {
        CONTEST_ID: contest_id,
        PROBLEM_ID: problem_id,
        TITLE: get_problem_title(soup),
        STATEMENT: get_problem_statement(soup),
        INPUT_SPEC: get_input_spec(soup),
        OUTPUT_SPEC: get_output_spec(soup)
    }

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

def map_to_contest(cf_response):
    return [Contest(contest['name'], contest['phase'], contest['id']) for contest in cf_response['result']]

def map_to_problem(cf_response):
    return [Problem(problem['index'], problem['contestId'], problem['name']) for problem in cf_response['result']['problems']]


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
def load_problems():
    return cf_api.get_problems()

@load_and_store_response(CF_CONTESTS, map_to_contest)
def load_contests():
    return cf_api.get_contests()


def parse_args():
    args = argparse.ArgumentParser(description='Utility to scrap information from Codeforces')

    args.add_argument('--force-download-of-problems', help='Self explanatory', action='store_true')
    args.add_argument('--force-download-of-contests', help='Self explanatory', action='store_true')

    return args.parse_args()

def main():
    args = parse_args()
    print('Loading problems from CF...')
    problems = load_problems(force_reload=args.force_download_of_problems)
    print('✅ Done')
    print('Loading contests from CF...')
    contests = load_contests(force_reload=args.force_download_of_contests)
    print('✅ Done')
    print(type(problems))
    print(problems[:5])
    print(contests[:5])
    existing_problem_ids = set()
    try:
        with open(DATASET_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_problem_ids.add((row[CONTEST_ID], row[PROBLEM_ID]))
    except FileNotFoundError:
        print('Dataset file does not exist. Creating it')

    with open(DATASET_FILE, 'a+') as f:
        writer = csv.DictWriter(f, fieldnames=[CONTEST_ID, PROBLEM_ID, TITLE, STATEMENT, INPUT_SPEC, OUTPUT_SPEC])
        if len(existing_problem_ids) == 0:
            writer.writeheader()

        with open(INPUT_FILE, 'r+') as f:
            reader = csv.DictReader(f)
            for input_row in reader:
                if (input_row[CONTEST_ID], input_row[PROBLEM_ID]) not in existing_problem_ids:
                    print('Processing:', input_row[CONTEST_ID], input_row[PROBLEM_ID])
                    try:
                        writer.writerow(get_problem_details(input_row[CONTEST_ID], input_row[PROBLEM_ID]))
                    except Exception as e:
                        print('Failed to process:', input_row[CONTEST_ID], input_row[PROBLEM_ID])
                        print(e)
                else:
                    print('Problem already processed:', input_row[CONTEST_ID], input_row[PROBLEM_ID])
if __name__ == '__main__':
    main()
    # pprinter = pprint.PrettyPrinter()
    # pprinter.pprint(get_problem_details(282, 'A'))
