from os import fdopen, remove
from shutil import move, copymode
from tempfile import mkstemp


def replace(file_path, pattern, subst):
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))

    copymode(file_path, abs_path)
    remove(file_path)
    move(abs_path, file_path)
