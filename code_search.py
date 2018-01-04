def code_file_handler(code):
    code.write_file()


def code_search(github, config):
    code_files = github.collect(config['keyword'])
    code_files.for_each(lambda code: code_file_handler(code))
