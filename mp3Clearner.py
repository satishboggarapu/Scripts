import os
from mp3_tagger import *

# path = '/Users/satishboggarapu/Music/iTunes/iTunes Media/Music/Sai Dharam Tej, Regina'
KEYWORDS_FILE_NAME = "keywords.txt"
KEYWORDS = []
file_types = ('.mp3', '.m4a')

paths = ['/Users/satishboggarapu/Music/iTunes/iTunes Media/Music/Ram, Keerthi Suresh/Nenu Sailaja']


def main():
    load_key_words()
    file_path = str(input("Enter album directory: "))
    # for file_path in paths:
    files = get_list_of_mp3_files_in_path(file_path)
    clean_files(files)


def clean_files(files):
    for file in files:
        clean_file(file)
        clean_file_name(file)


def clean_file(file):
    print(file)
    mp3_file = MP3File(file)
    mp3_file.set_version(VERSION_2)

    mp3_file.album = clean_string(mp3_file.album)
    mp3_file.song = clean_string(mp3_file.song)
    mp3_file.genre = "Telugu"
    mp3_file.comment = ""
    # mp3_file.band = clean_string(mp3_file.band)
    # mp3_file.composer = clean_string(mp3_file.composer)
    mp3_file.copyright = ""
    mp3_file.publisher = ""
    mp3_file.url = " "
    mp3_file.save()
    tags = mp3_file.get_tags()
    print(tags)


def clean_string(string):
    clean_string = string
    for word in KEYWORDS:
        clean_string = clean_string.replace(word, "")
    return clean_string.strip()


def clean_file_name(file):
    file_split = file.split('/')
    file_name = file_split[-1]
    file_extension = file_name[-4:]
    file_raw_name = file_name[:-4]
    file_name_clean = clean_string(file_raw_name)
    file_split[-1] = file_name_clean + file_extension
    new_file_path = '/'.join(file_split)
    os.rename(file, new_file_path)


###############################################


def get_list_of_mp3_files_in_path(path):
    files = []
    for root, directories, fileNames in os.walk(path):
        for filename in fileNames:
            if filename.endswith(file_types):
                files.append(os.path.join(root, filename))
    return files


def load_key_words():
    global KEYWORDS
    with open(KEYWORDS_FILE_NAME, 'r') as file:
        KEYWORDS = file.read().splitlines()



if __name__ == "__main__":
    main()