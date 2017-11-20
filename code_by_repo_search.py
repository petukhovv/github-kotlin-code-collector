from pprint import pprint

from code_search import code_file_handler


def repo_handler(repo, config):
    code_files_set = repo.search_code('fun')
    code_files_set.for_each(lambda code: code_file_handler(code, config))


def code_by_repo_search(github, config):
    repos = github.collect_repo()
    repos.for_each(lambda repo: repo_handler(repo, config))
