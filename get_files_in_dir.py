import glob
import re

path = "mazes/"


# pass a filetype or * to get all files in dir
def get_files_in_dir(fileformat: str, recursive: bool) -> list:
    files = [f for f in glob.glob(path + "*." + fileformat, recursive=recursive)]
    return files


def new_file_num(path: str) -> int:
    path = path
    # returns a list of files in mazes folder
    files = [f for f in glob.glob(path + "*.*", recursive=False)]
    # lambda function splits the files string by dot and slash returning just the filename
    filenames = list(map(lambda x: x.split(".")[0].split("/")[1], files))
    # lambda function returns just the digits after 'maze' in the filename
    numbers = list(
        filter(
            lambda x: x.isdigit(),
            map(lambda x: x.split("maze")[1].split("_")[0], filenames),
        )
    )

    if numbers:
        # find the highest number in the list
        highest_num = max(int(num) for num in numbers)
    else:
        highest_num = 0
    new_file_num = highest_num + 1

    return new_file_num


files = get_files_in_dir("*", recursive=False)

# print a numbered, tabbed list of files
for idx, file in enumerate(files):
    print("{}.\t{}".format(idx + 1, file))


print("new filename: ", new_file_name())
