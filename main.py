import argparse

from lib.GithubCodeCollector import GithubCodeCollector
from code_search import code_search
from code_by_repo_search import code_by_repo_search
from lib.helpers.TimeLogger import TimeLogger

parser = argparse.ArgumentParser()
parser.add_argument('--keyword', '-k', nargs=1, type=str, help='keyword for search on Github')
parser.add_argument('--token', '-t', nargs=1, type=str, help='Github token')
parser.add_argument('--directory', '-d', nargs=1, type=str, help='directory for saving Kotlin source code files')

args = parser.parse_args()
keyword = args.keyword[0]
token = args.token[0]
directory = args.directory[0]

LOG_FILE = 'log.txt'

github = GithubCodeCollector(token)

config = {
    'log_file': LOG_FILE,
    'keyword': keyword,
    'directory': directory
}

time_logger = TimeLogger()

# code_search(github, config)
code_by_repo_search(github, config)

time_logger.finish('Code collection')
