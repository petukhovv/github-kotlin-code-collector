from lib.helper.AstHelper import AstHelper
from lib.GithubCodeCollector import GithubCodeCollector
from lib.helper.TimeLogger import TimeLogger

compiler_path = '...'
kt_code_temp_file = 'code.kt'
log_file = 'log.txt'

github = GithubCodeCollector('github_token')
code_files = github.collect('fun')


def code_file_handler(code):
    """
    Collection of files with Kotlin code from Github, their parsing and resulting AST conversion to JSON
    """
    getting_content_time = code.write_file(kt_code_temp_file)
    compilation_time = code.compile(compiler_path)
    code.remove_file()
    transformation_time = AstHelper.text2json(code)

    times = [getting_content_time, compilation_time, transformation_time]
    prefix = str(code.number) + '|' + code.obj.html_url + '|' + str(code.obj.size)
    TimeLogger.console_output(times, prefix=prefix)
    TimeLogger.file_output(log_file, times, prefix=prefix)


code_files.for_each(code_file_handler)
