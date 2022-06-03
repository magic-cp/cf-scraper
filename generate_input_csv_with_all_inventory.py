"""
Generate input csv with all codeforces problems
"""

import csv
import common
import compute_dataset_with_input

def main():
    args = common.parse_args()
    with open(compute_dataset_with_input.INPUT_FILE, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=[compute_dataset_with_input.PROBLEM_ID, compute_dataset_with_input.CONTEST_ID])
        writer.writeheader()
        for problem in common.load_problems(force_reload=args.force_download_of_problems):
            writer.writerow({
                compute_dataset_with_input.PROBLEM_ID: problem.index,
                compute_dataset_with_input.CONTEST_ID: problem.contest_id
            })

if __name__ == '__main__':
    main()