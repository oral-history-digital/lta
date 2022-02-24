import os
from pathlib import Path

IGNORED_EXTENSIONS = {'', '.ods'}

path = '/mnt/trove.storage.fu-berlin.de/ohd-av/bas_packages/adg'

def filename_to_ext(name):
    file_path = os.path.join(path, name)
    extension = Path(file_path).suffix
    return extension


def extensions_for_directory(dir_name):
    dir_path = os.path.join(path, name)
    filenames = os.listdir(dir_path)
    extensions = set(map(filename_to_ext, filenames))
    ext_wo_ignored = extensions - IGNORED_EXTENSIONS
    return list(ext_wo_ignored);


directory_names = os.listdir(path)

for name in directory_names:
    if not os.path.isdir(os.path.join(path, name)):
        directory_names.remove(name)

directory_names.sort()


# for each directory, find out which extensions are used

directory_dict = {}

for name in directory_names:
    directory_dict[name] = extensions_for_directory(name)


extension_dict = {}

for name, extensions in directory_dict.items():
    for ext in extensions:
        if not ext in extension_dict:
            extension_dict[ext] = []

        extension_dict[ext].append(name)


# print everything

for ext, archive_ids in extension_dict.items():
    print(ext, archive_ids, len(archive_ids))

all_archive_ids = []

for archive_ids in extension_dict.values():
    all_archive_ids += archive_ids

print(all_archive_ids)

print(len(set(all_archive_ids)))
