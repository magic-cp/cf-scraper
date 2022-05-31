from common import default_argument_parser, load_problems, Problem
from typing import List


def compute_tags_stats(problems: List[Problem]):
    problems_by_tag = {}
    for problem in problems:
        for tag in problem.tags:
            if tag not in problems_by_tag:
                problems_by_tag[tag] = []
            problems_by_tag[tag].append(problem)

    return dict(sorted(problems_by_tag.items(), key=lambda tag: len(tag[1]), reverse=True))


def main():

    args = default_argument_parser().parse_args()

    print('Loading problems from CF...')

    problems = load_problems(force_reload=args.force_download_of_problems)

    problems_by_tag = compute_tags_stats(problems)
    for i, tag in enumerate(problems_by_tag, 1):
        print(f'#{i} {tag}: {len(problems_by_tag[tag])} problems')

        problems_by_tag[tag].sort(key=lambda problem: problem.solved_count, reverse=True)
        top = 10
        print(f'{top} most solved problem')
        for problem in problems_by_tag[tag][:top]:
            print(f'{problem} with {problem.solved_count} successful submissions. {problem.get_url()}')


if __name__ == '__main__':
    main()