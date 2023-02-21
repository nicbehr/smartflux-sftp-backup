import errno
import os
import logging
import posixpath
import stat
from paths import DATA_PATH, REMOTE_DATA_PATH
import pysftp
import logging_util as l

logger = logging.getLogger(__name__)
remote_dir_names = []

def listdir_ignorezip(sftp, remotepath):
    """
    Cycles through a sftp remote directory and yields folders which are not zip or ghg folders

    Args:
        sftp (sftp.Connection): The pysftp connection
        remotepath (str): The path to cycle

    Yields:
        str: path name of a folder that is not a zip or ghg file
    """
    for f in sftp.listdir(remotepath):
        if not f.endswith(".zip") and not f.endswith(".ghg"):
            yield f

def get_local_filedict(path):
    owd = os.getcwd()
    filedict = {}
    try:
        os.chdir(path)
        for path, dirs, files in os.walk("."):
            path_posix = path.replace(os.sep, posixpath.sep)
            filedict[path_posix] = []
        for key in filedict:
            filedict[key] = [f for f in os.listdir(key) if os.path.isfile(os.path.join(key, f))]
    finally:
        os.chdir(owd)
    return filedict

# call back function for the walk_remote_dirs function
def store_dir_name(dirname):
    remote_dir_names.append(dirname)

def walk_remote_dirs(sftp, remotepath, dcallback, recurse=True):
    try:
        entries = listdir_ignorezip(sftp, remotepath)
    except IOError as e:
        logger.error("Exception: {0}".format(e))
        if e.errno != errno.EACCES:
            raise
        else:
            entries = []

    for entry in entries:
        pathname = posixpath.join(remotepath, entry)
        mode = sftp.stat(pathname).st_mode
        if stat.S_ISDIR(mode):
            # It's a directory, call the dcallback function
            dcallback(pathname)
            if recurse:
                # now, recurse into it
                walk_remote_dirs(sftp, pathname, dcallback)
    
    return remote_dir_names

def make_local_path(dir, filename):
    return DATA_PATH + dir[2:len(dir)]+"/"+filename

def create_path(path, dir):
    owd = os.getcwd()
    try:
        logger.info(str(dir) + " not in folders, attempting to create it")
        os.chdir(path)
        os.makedirs(dir, exist_ok=True)
    finally:
        os.chdir(owd)

def download_file(directory: str, filename:str, sftp:pysftp.Connection):
    remotepath = str(directory)+"/"+filename
    localpath = make_local_path(directory, filename)
    l.LOG_DOWNLOAD_INFO(logger, filename, remotepath, localpath)
    try:
        sftp.get(remotepath=filename, localpath=localpath, preserve_mtime=True)
        l.LOG_DOWNLOAD_SUCCESFUL
    except:
        l.LOG_GET_ERROR(logger, filename)
