import os
import subprocess

from github import Github, GithubException
from pprint import pprint

from lib.helpers.TimeLogger import TimeLogger
from lib.helpers.ContentSaver import ContentSaver


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
    factor = 1000

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
        self.filename = None

    def write_file(self, filename=None, is_measure_time=True):
        self.filename = filename
        if is_measure_time:
            time_logger = TimeLogger()

        try:
            content = self.obj.decoded_content.decode('utf-8')
        except GithubException:
            print('404 error! File is skipped.')
            return None

        if filename is None:
            ContentSaver.save(self.folder, self.number, content, ext='kt')
        else:
            f = open(filename, 'w')
            f.write(content)
            f.close()

        if is_measure_time:
            return time_logger.finish()

    def compile(self, compiler_path, is_measure_time=True):
        if self.filename is None:
            raise Exception('Not specified filename')

        if is_measure_time:
            time_logger = TimeLogger()
        subprocess.call([compiler_path, self.filename])
        if is_measure_time:
            return time_logger.finish()

    def remove_file(self):
        if self.filename is not None:
            os.remove(self.filename)
