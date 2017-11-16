import math


class PathHelper:
    @staticmethod
    def calculate(id, start=True, max_files_in_dir=100):
        """
        Calculate path contains hierarchy dirs by id
        Example input: 9366462
        Example output: 9/36/64/62 (at a max_files_in_dir = 100)
        """
        dividing = math.floor(id / max_files_in_dir)
        modulo = id % max_files_in_dir
        if dividing > max_files_in_dir:
            dirs_part = PathHelper.calculate(dividing, False, max_files_in_dir) + '/' + str(dividing % 100)
        else:
            dirs_part = str(dividing)

        if start:
            file_part = '/' + str(modulo)
        else:
            file_part = ''

        return dirs_part + file_part


