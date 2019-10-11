import glob
import re

path = "mazes/"


# pass a filetype or * to get all files in dir
def get_files_in_dir(fileformat: str, recursive: bool) -> list:
    files = [f for f in glob.glob(path + "*." + fileformat, recursive=recursive)]
    return files


def new_file_name(files):
    numbers = re.findall(r"\d+", ", ".join(files))
    highest_num = max(int(num) for num in numbers)
    new_file_name = "maze{}.json".format(highest_num + 1)
    return new_file_name


files = get_files_in_dir("*", recursive=False)

# print a numbered, tabbed list of files
for idx, file in enumerate(files):
    print("{}.\t{}".format(idx + 1, file))


print("new filename: ", new_file_name(files))
