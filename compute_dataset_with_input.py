import csv
import os
import requests

from bs4 import BeautifulSoup


PROBLEM_STATEMENT_SELECTOR = '.problem-statement'
TITLE_SELECTOR = PROBLEM_STATEMENT_SELECTOR + ' .title'
STATEMENT_SELECTOR = PROBLEM_STATEMENT_SELECTOR + ' .header + div'
INPUT_SPECIFICATION_SELECTOR = PROBLEM_STATEMENT_SELECTOR + ' .input-specification'
OUTPUT_SPECIFICATION_SELECTOR =  PROBLEM_STATEMENT_SELECTOR + ' .output-specification'
TAG_SELECTOR = 'span.tag-box'

DATASET_FILE = os.path.join('dataset', 'cf_problems.csv')
INPUT_FILE = os.path.join('dataset', 'input.csv')

CONTEST_ID = 'contest_id'
PROBLEM_ID = 'problem_id'
TITLE = 'title'
STATEMENT = 'statement'
INPUT_SPEC = 'input_spec'
OUTPUT_SPEC = 'output_spec'
URL_KEY = 'url'
TAGS = 'tags'

CSV_FIELDNAMES = [CONTEST_ID, PROBLEM_ID, TITLE, STATEMENT, INPUT_SPEC, OUTPUT_SPEC, URL_KEY, TAGS]

CF_PROBLEMS = 'input/problems.json'
CF_CONTESTS = 'input/contests.json'

def get_csv_reader(file_name):
    with open(file_name, 'w+') as csv_file:
        return csv.DictReader(csv_file)

def get_csv_writer(file_name):
    with open(file_name, 'w+') as csv_file:
        return csv.DictWriter(csv_file, fieldnames=CSV_FIELDNAMES)

def get_problem_title(soup: BeautifulSoup):
    # we splice because the problem title has the problem id in it e.g. "A. Bit++"
    return soup.select_one(TITLE_SELECTOR).text[3:]

def get_problem_statement(soup: BeautifulSoup):
    return soup.select_one(STATEMENT_SELECTOR).text

def get_input_spec(soup: BeautifulSoup):
    return soup.select_one(INPUT_SPECIFICATION_SELECTOR).text

def get_output_spec(soup: BeautifulSoup):
    return soup.select_one(OUTPUT_SPECIFICATION_SELECTOR).text

def get_tags(soup: BeautifulSoup):
    tags = []
    for tag in soup.select(TAG_SELECTOR):
        tags.append(tag.text.strip())
    return ';'.join(tags)

def get_problem_details(contest_id, problem_id):

    url = f"https://codeforces.com/contest/{contest_id}/problem/{problem_id}"

    page = requests.get(url)


    soup = BeautifulSoup(page.content, "html.parser")

    return {
        CONTEST_ID: contest_id,
        PROBLEM_ID: problem_id,
        TITLE: get_problem_title(soup),
        STATEMENT: get_problem_statement(soup),
        INPUT_SPEC: get_input_spec(soup),
        OUTPUT_SPEC: get_output_spec(soup),
        URL_KEY: url,
        TAGS: get_tags(soup)
    }

def main():
    existing_problem_ids = set()
    try:
        with open(DATASET_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_problem_ids.add((row[CONTEST_ID], row[PROBLEM_ID]))
    except FileNotFoundError:
        print('Dataset file does not exist. Creating it')

    with open(DATASET_FILE, 'a+', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        if len(existing_problem_ids) == 0:
            writer.writeheader()

        with open(INPUT_FILE, 'r+') as f:
            reader = csv.DictReader(f)
            for input_row in reader:
                if (input_row[CONTEST_ID], input_row[PROBLEM_ID]) not in existing_problem_ids:
                    print('Processing:', input_row[CONTEST_ID], input_row[PROBLEM_ID])
                    try:
                        problem_details = get_problem_details(input_row[CONTEST_ID], input_row[PROBLEM_ID])
                        print('Problem info', problem_details)
                        writer.writerow(problem_details)
                    except Exception as e:
                        print('Failed to process:', input_row[CONTEST_ID], input_row[PROBLEM_ID])
                        print(e)
                else:
                    print('Problem already processed:', input_row[CONTEST_ID], input_row[PROBLEM_ID])

if __name__ == '__main__':
    main()
