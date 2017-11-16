import os
import subprocess

from github import Github

from lib.helpers.TimeLogger import TimeLogger
from lib.helpers.ContentSaver import ContentSaver


class GithubCodeCollector:
    def __init__(self, token):
        self.github = Github(token)

    def collect(self, keywords, sort='indexed', order='desc'):
        codes = self.github.search_code(keywords + ' language:kotlin', sort=sort, order=order)
        return GithubCodeFilesSet(codes)


class GithubCodeFilesSet:
    def __init__(self, codes):
        self.codes = codes

    def for_each(self, callback):
        file_number = 1
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

        content = self.obj.decoded_content.decode('utf-8')

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
