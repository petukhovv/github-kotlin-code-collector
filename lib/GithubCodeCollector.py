import os

from github import Github, RateLimitExceededException, UnknownObjectException
from pprint import pprint

from lib.helpers.TimeLogger import TimeLogger
from lib.helpers.ContentSaver import ContentSaver
import time


class GithubCodeCollector:
    def __init__(self, token):
        self.github = Github(token)

    def collect(self, keywords, sort='indexed', order='desc', part_number=1):
        codes = self.github.search_code(keywords + ' language:kotlin', sort=sort, order=order)
        return GithubCodeFilesSet(codes, part_number)

    def collect_repo(self, sort='stars', order='desc'):
        repos = self.github.search_repositories('language:kotlin', sort=sort, order=order)
        return GithubRepoSet(repos, self)


class GithubRepoSet:
    def __init__(self, repos, gcc):
        self.repos = repos
        self.gcc = gcc

    def for_each(self, callback):
        repo_number = 1
        for repo in self.repos:
            callback(GithubRepo(repo, self.gcc, repo_number))
            repo_number += 1


class GithubRepo:
    def __init__(self, repo, gcc, repo_number):
        self.obj = repo
        self.gcc = gcc
        self.number = repo_number

    def search_code(self, keywords, sort='indexed', order='desc'):
        return self.gcc.collect(keywords + ' repo:' + self.obj.full_name, sort, order, self.number)


class GithubCodeFilesSet:
    factor = 100000     # factor for making unique part_number within all repos

    def __init__(self, codes, part_number):
        self.codes = codes
        self.part_number = part_number

    def for_each(self, callback):
        file_number = 1 * self.part_number * self.factor
        for code in self.codes:
            callback(GithubCodeFile(code, file_number))
            file_number += 1


class GithubCodeFile:
    folder = 'code'

    def __init__(self, code, file_number):
        self.obj = code
        self.number = file_number

    def write_file(self):
        time_logger = TimeLogger()

        try:
            content = self.obj.decoded_content.decode('utf-8')
        except Exception as e:
            pprint(e)
            if isinstance(e, RateLimitExceededException):
                print('File is skipped. Waiting for 1 minute.')
                with open('rate_limit_exceeded_exceptions.log', 'a') as exceptions_descriptor:
                    exceptions_descriptor.write(self.number + os.linesep)
                time.sleep(60)
                return self.write_file()
            elif isinstance(e, UnknownObjectException):
                print('File is skipped because not found.')
                with open('unknown_object_exceptions.log', 'a') as exceptions_descriptor:
                    exceptions_descriptor.write(self.number + os.linesep)
            return None

        path = ContentSaver.save(self.folder, self.number, content, ext='kt')

        time_logger.finish('Write ' + path + ' (#' + str(self.number) + ') file')
