import os
import shutil
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from flask import current_app as app
from pathlib import Path
from main import cache


class NodePath():
    def __init__(self, original, sanitized, stripped_original):
        self.original = original
        self.sanitized = sanitized
        self.stripped_original = stripped_original
    
    def get_link(self):
        link = sanitize_path(self.stripped_original)
        if not self.is_file():
            link += "/"

        return link
    
    def split_directories(self, remove_last=True):
        split = self.stripped_original.split("/") #remove last element of the array
        return split if not remove_last else split[:-1]
        
    def get_current_directory(self):
        return self.stripped_original.split("/")[-1] #get last element of the array

    def is_file(self):
        return os.path.isfile(self.original)

    def is_image(self):
        if not self.is_file():
            return False

        filename, file_extension = os.path.splitext(self.original)
        return file_extension in [ ".jpg", ".jpeg", ".png", ".bmp", ".gif" ]

    def get_file_name(self):
        head, tail = os.path.split(self.original)
        return tail 

    def convert_to_title(self):
        return " - ".join( self.stripped_original.split("/")[-2:] )
    
    def __repr__(self):
        return "<NodePath {}>".format(self.original)


def download_and_unzip_source():
    global compiled_file_paths

    
    resp = urlopen(os.environ["zip_file_url"])
    zipfile = ZipFile(BytesIO(resp.read())) 

    shutil.rmtree(os.environ["zip_file_folder"]) #Remove existing folder
    zipfile.extractall() #Extract zip

    compiled_file_paths = compile_paths()


"""
Insensitive LS
"""
@cache.memoize(60 * 60 * 24)
def get_ls(path_obj):
    try:
        ls = os.listdir(path_obj.original)
        result = []
        for x in ls:
            full_path = path_obj.original + "/" + x

            file = [ x for x in compiled_file_paths if x.original == full_path ][0]
            if file.get_file_name() == "Medya":
                continue
            
            result.append(file)
        
        return result


    except Exception as exc:
        print(exc)
        return None


def get_content(path_obj):
    return open(path_obj.original).read()


def path_exists(path):
    path = sanitize_path(os.environ["zip_file_folder"] + "/" + path) #sanitize path

    if not path in [ x.sanitized for x in compiled_file_paths ]: #check if path is in compiled file paths
        return False, None

    file = [ x for x in compiled_file_paths if x.sanitized == path ][0] #if it is, select it

    return True, file


def compile_paths():
    all_paths = Path(os.environ["zip_file_folder"] + "/").glob("**/*")
    compiled = []

    for path in all_paths:
        str_path = str(path)

        sanitized_path = sanitize_path(str_path)

        compiled.append(NodePath(str_path, sanitized_path, str_path.replace(os.environ["zip_file_folder"] + "/", "").replace(".md", "")))

    return compiled


def sanitize_path(path):
    change_list = [ ("İ", "i"), ("Ş", "ş"), ("Ü", "ü"), ("Ğ", "ğ") ]
    for x in change_list:
        a, b = x
        path = path.replace(a, b)
    
    return path.replace(" ", "-").replace(".md", "").lower()


def get_media(name):
    filtered = [ x for x in compiled_file_paths if x.get_file_name() == name and x.is_image() ]
    if len(filtered) < 1:
        return None

    return filtered[0]


compiled_file_paths = compile_paths()