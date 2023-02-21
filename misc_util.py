from datetime import datetime
import os, shutil
from paths import * 

def write_datetime():
    now = datetime.now()
    f = open('last_timestamp.txt', "w")
    f.write(str(now))
    f.close()

def write_copied_files(copied_files:list):
    now = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    path = COPIED_FILES_PATH
    txt_file = 'copied_files_'+str(now)+'.txt'
    owd = os.getcwd()
    os.chdir(path)
    with open(txt_file, "w+") as f:
        f.write(str(now) +" \n")
        for file in copied_files:
            f.write("%s \n" % file)
    os.chdir(owd)
    return str(path)+str(txt_file)

def read_datetime():
    f = open('last_timestamp.txt', "r")
    timestamp = datetime.strptime(f.read(), '%Y-%m-%d %H:%M:%S.%f')
    f.close()
    return timestamp

def clean_temp_folder():
    for filename in os.listdir(TEMPPATH):
        file_path = os.path.join(TEMPPATH, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
            