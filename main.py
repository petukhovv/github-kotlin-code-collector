import sys

from lib.helpers.AstHelper import AstHelper
from lib.GithubCodeCollector import GithubCodeCollector
from lib.helpers.TimeLogger import TimeLogger

compiler_path = '...'
kt_code_temp_file = 'code.kt'
log_file = 'log.txt'

github = GithubCodeCollector('17ecf0c4d6ab960bdbde76609747852c3e435ce9')
code_files = github.collect('fun')

no_compile = True if '--no-compile' in sys.argv else False


def code_file_handler(code):
    """
    Collection of files with Kotlin code from Github, and either:
        1) their parsing and resulting AST conversion to JSON;
        2) or just saving in .kt file (if --no-compile option is specified).
    """
    getting_content_time = code.write_file(None if no_compile else kt_code_temp_file)
    if not no_compile:
        compilation_time = code.compile(compiler_path)
        code.remove_file()
        transformation_time = AstHelper.text2json(code)

    times = [getting_content_time]
    if not no_compile:
        times.append(transformation_time, compilation_time)
    prefix = str(code.number) + '|' + code.obj.html_url + '|' + str(code.obj.size)
    TimeLogger.console_output(times, prefix=prefix)
    TimeLogger.file_output(log_file, times, prefix=prefix)


code_files.for_each(code_file_handler)
