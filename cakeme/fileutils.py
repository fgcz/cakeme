import os
import zipfile


def make_path_to_file(pathandfile):
    if not os.path.exists(os.path.dirname(pathandfile)):
        os.makedirs(os.path.dirname(pathandfile))

def remove_files_from_folder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e


def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def zip_dir(path, out_zip):
    ziph = zipfile.ZipFile(out_zip, 'w')
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
    ziph.close()
