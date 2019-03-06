import zipfile
import os
import pathlib
import shutil

desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
# directory of unzipped files
unzip_directory = desktop + "/icon"
# icon directory
icon_directory = desktop + "/"

icon_image_sizes = ['24dp', '36dp', '48dp']
icon_name_size_postfix = ['_24dp', '_36dp', '_48dp']
icon_imageset_folder_postfix = ['_24dp.imageset', '_36dp.imageset', '_48dp.imageset']
drawable_folders = ['/drawable-mdpi/', '/drawable-xhdpi/', '/drawable-xxhdpi/']
icon_scale_postfix = ['', '_2x', '_3x']


def main():
    zip_file_name = str(input("Enter the icon zip file directory: "))
    if zipfile.is_zipfile(zip_file_name):
        file = zipfile.ZipFile(zip_file_name)
        file.extractall(unzip_directory)
        file.close()
        create_icon_image_sets(zip_file_name[0: -4])
        shutil.rmtree(unzip_directory)
    else:
        print("Invalid file.")


def create_icon_image_sets(folder_name):
    global icon_directory
    # get icon name
    icon_name = get_icon_name()

    ### create icon folder
    icon_directory += icon_name
    # remove if already exists
    if os.path.exists(icon_directory):
        shutil.rmtree(icon_directory)
    os.makedirs(icon_directory)

    # create imageset folders
    create_imageset_folders(icon_name)

    # copy images
    for i in range(len(drawable_folders)):
        path = unzip_directory + drawable_folders[i]
        copy_images(path, icon_name, icon_scale_postfix[i])

    # create json file
    for i in range(len(icon_imageset_folder_postfix)):
        path = icon_directory + "/" + icon_name + icon_imageset_folder_postfix[i]
        create_json_file(path, icon_name + icon_name_size_postfix[i])


def create_json_file(file_path, icon_name):
    path = file_path + "/Contents.json"
    json_file = open(path, "w")
    json_file.writelines(get_json_file_content(icon_name))
    json_file.close()

def copy_images(file_path, icon_name, multiplier):
    new_path = icon_directory + "/" + icon_name
    for root, dirs, files in os.walk(file_path):
        for file in files:
            if "black" in file:
                des_path = new_path
                src_path = file_path + file
                for i in range(len(icon_image_sizes)):
                    if icon_image_sizes[i] in file:
                        des_path += icon_imageset_folder_postfix[i] + "/" + icon_name + icon_name_size_postfix[i] + multiplier + '.png'
                        shutil.copy(src_path, des_path)
                        break


def create_imageset_folders(icon_name):
    for postfix in icon_imageset_folder_postfix:
        dir_path = icon_directory + "/" + icon_name + postfix
        # todo check if dir exists first
        os.makedirs(dir_path)


def get_icon_name():
    file_path = unzip_directory + "/drawable-mdpi/"
    for root, dirs, files in os.walk(file_path):
        for file in files:
            if "black" in file:
                endIndex = file.index("black") - 1
                return file[0:endIndex]


def get_json_file_content(icon_name):
    file_content = """{
    "images": [
        {
            "filename": "icon_name.png",
            "idiom": "universal",
            "scale": "1x"
        },
        {
            "filename": "icon_name_2x.png",
            "idiom": "universal",
            "scale": "2x"
        },
        {
            "filename": "icon_name_3x.png",
            "idiom": "universal",
            "scale": "3x"
        }
    ],
    "info": {
        "author": "xcode",
        "version": 1
    }
}"""
    file_content = file_content.replace("icon_name", icon_name)
    return file_content


if __name__ == "__main__":
    main()
