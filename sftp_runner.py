# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 09:58:10 2022

@author: Nicolas Behrens
"""

import pysftp
from dotenv import load_dotenv, find_dotenv
from os import getenv
import os 
import logging
import logging_util as l
from sftp_utils import create_path, download_file, get_local_filedict, store_dir_name, walk_remote_dirs
from paths import * 

load_dotenv(find_dotenv())

# Get constants
HOSTNAME = getenv('HOSTNAME')
USERNAME = getenv('ECUSER')
PASSWORD = getenv('ECPASSWORD')
PORT = int(getenv('PORT'))

FILEEXTENSIONS = ['.txt', '.ghg', '.jpg', '.zip', '.log']
local_files = get_local_filedict(DATA_PATH)

# instantiate logger
logger = logging.getLogger(__name__)

# get current working directory
owd = os.getcwd()

# initiate lists to be filled
remote_dir_names = []
copied_files = []

def handle_file(dir:str, filename:str, sftp:pysftp.Connection):
    # TODO
    # Implemente comparison of file sizes, made program break because of wrong cd
    #remote_file_bigger_than_local_file = (sftp.stat(filename).st_size > os.stat(str(dir)+str(filename)).st_size) #TODO: Check correct local path
    #logger.info("Handling file: " + str(filename))
    if any(filename.endswith(s) for s in FILEEXTENSIONS):
        if dir not in local_files:
            create_path(DATA_PATH, dir)
            local_files[dir] = []
        if (filename not in local_files[dir]):
            l.LOG_FILENOTLOCAL_INFO
            download_file(dir, filename, sftp)
            copied_files.append(filename)
        # elif (remote_file_bigger_than_local_file):
        #     l.LOG_LOCALFILEOVERWRITE_INFO(logger, filename)
        #     download_file()
        #     copied_files.append(filename)
        #else:
            #logger.info("File already in backup")
    else:
        logger.info("File/folder ignored due to wrong extension")


def run_backup(sftp:pysftp.Connection, remote_dir_names:list):
    """
    Runs the actual backup process

    Args:
        sftp (pysftp.Connection): The pysftp connection
        remote_dir_names (list): List of remote directories to backup
    """
    logger.info("=================== Starting backup process =================== ")
    for dir in remote_dir_names:

        logger.info("Entering directory: " + str(dir))
        try:
            with sftp.cd(dir):
                logger.info("Entered directory: " + str(dir))
                for filename in sftp.listdir('.'):
                    handle_file(dir, filename, sftp)
        except:
            l.LOG_ERROR(logger)
    logger.info("Backup process complete, closing connection")


def start_process():
    """
    Top level wrapper for the backup process

    Returns:
        list:str: List of files that have been copied from remote to local
    """
    cnopts = pysftp.CnOpts(knownhosts=KNOWN_HOSTS_PATH)

    cnopts.log = CNOPTS_LOG_PATH
    try:
        with pysftp.Connection(HOSTNAME, username=USERNAME, password=PASSWORD, port=PORT, cnopts=cnopts) as sftp:
            logger.info("Entering " + str(REMOTE_DATA_PATH))
            try:
                with sftp.cd(REMOTE_DATA_PATH):
                    logger.info("Starting dir walk")
                    remote_dir_names = walk_remote_dirs(sftp,".",store_dir_name,recurse=True)
                    logger.info("Finished walking dirs")
                    run_backup(sftp, remote_dir_names)
            except:
                l.LOG_ERROR(logger)
        logger.info("Closing session")
        sftp.close()
    except:
        l.LOG_CONNECTION_ERROR(logger)
    return copied_files