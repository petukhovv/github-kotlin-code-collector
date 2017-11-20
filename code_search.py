from lib.helpers.TimeLogger import TimeLogger
from lib.helpers.AstHelper import AstHelper


def code_file_handler(code, config):
    """
    Collection of files with Kotlin code from Github, and:
        1) either their parsing and resulting AST conversion to JSON;
        2) or just saving in .kt file (if --no-compile option is specified).
    """
    getting_content_time = code.write_file(None if config['no_compile'] else config['kt_code_temp_file'])
    if getting_content_time is None:
        return
    if not config['no_compile']:
        compilation_time = code.compile(config['compiler_path'])
        code.remove_file()
        transformation_time = AstHelper.text2json(code)

    times = [getting_content_time]
    if not config['no_compile']:
        times.append(transformation_time, compilation_time)
    prefix = str(code.number) + '|' + code.obj.html_url + '|' + str(code.obj.size)
    TimeLogger.console_output(times, prefix=prefix)
    TimeLogger.file_output(config['log_file'], times, prefix=prefix)


def code_search(github, config):
    code_files = github.collect('fun')
    code_files.for_each(lambda code: code_file_handler(code, config))
