"""
Utilities to scrap the problem details of a codeforces problem.

Date created: 2022-05-16
Date of when codeforces was studied for scraping: 2022-05-16
"""
import requests
import pprint

from bs4 import BeautifulSoup

PROBLEM_STATEMENT_SELECTOR = '.problem-statement'
TITLE_SELECTOR = ".title"
STATEMENT_SELECTOR = '.header + div'
INPUT_SPECIFICATION_SELECTOR = '.input-specification'
OUTPUT_SPECIFICATION_SELECTOR = '.output-specification'


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

    print(soup)

    for elem in soup.select(TITLE_SELECTOR):
        print(elem.text)
        print(elem)
        print(type(elem))

    return {
        'contest_id': contest_id,
        'problem_id': problem_id,
        'title': get_problem_title(soup),
        'statement': get_problem_statement(soup),
        'input_spec': get_input_spec(soup),
        'output_spec': get_output_spec(soup)
    }

if __name__ == '__main__':

    pprinter = pprint.PrettyPrinter()
    pprinter.pprint(get_problem_details(282, 'A'))