import sys
import os
from pathlib import Path
import shutil
from src.markdown_to_html import generate_page

basepath = sys.argv[0]
if basepath == '':
    basepath = '/'


def main():
    global basepath
    copy_from_to("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
       
    entries = os.listdir(dir_path_content)

    for entry in entries:
        entry_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        if os.path.isfile(entry_path):
            generate_page(entry_path, template_path, Path(dest_path).with_suffix(".html"), basepath)
        else:
            generate_pages_recursive(entry_path, template_path, dest_path, basepath)


def copy_from_to(source, destination):
    if os.path.exists(source):
        delete_all_directory(destination)
        copy_all_directory(source, destination, 0)
    else:
        raise Exception(f"source \"{source}\" does not exist")

def delete_all_directory(directory):
    print(f"deleting the destination directory: {directory}")
    if os.path.exists(directory):
        shutil.rmtree(directory)
    print("successfully deleted \n")
    return

def copy_all_directory(source, destination, depth):
    tabs = "  " * depth
    print(f"{tabs}copying from \"{source}\" to \"{destination}\"")
    os.mkdir(destination)

    source_content = os.listdir(source)

    for item in source_content:
        item_path = os.path.join(source, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, destination)
            print(f"{tabs}succsessfully copied {item} to {destination}")
        else:
            print(f"\n{tabs}  recursion  ---------------------------------")
            new_dest = os.path.join(destination, item)
            copy_all_directory(item_path, new_dest, depth+1)

    print(f"{tabs}end recursion ----------------------------------\n")
    return





main()
