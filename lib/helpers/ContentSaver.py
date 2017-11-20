import os

from .PathHelper import PathHelper


class ContentSaver:
    @staticmethod
    def save(folder, file_number, content, ext='json'):
        """
        Calculate path contains hierarchy dirs by id
        Example input: 9366462
        Example output: 9/36/64/62 (at a max_files_in_dir = 100)
        """
        path = folder + '/' + PathHelper.calculate(file_number) + '.' + ext
        basename = os.path.basename(path)
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        f = open(dirname + '/' + basename, 'wb')
        f.write(content.encode('utf8'))
        f.close()
