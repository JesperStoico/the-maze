import glob

path = "mazes/"


def get_files_in_dir(fileformat: str, recursive: bool) -> list:
    files = [f for f in glob.glob(path + "*." + fileformat, recursive=recursive)]
    return files


# pass a filetype or * to get all files in dir
files = get_files_in_dir("*", recursive=True)
files.sort()

# print a numbered, tabbed list of files
for idx, file in enumerate(files):
    print("{}.\t{}".format(idx + 1, file))
