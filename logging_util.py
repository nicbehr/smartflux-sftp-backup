import sys
import logging
from datetime import datetime, timedelta
from datetime import datetime, timedelta
import glob
import gzip
from pathlib import Path
import shutil
import os
from paths import * 

def open_file(path):
    if Path(path).suffix == '.gz':
        return gzip.open(path, mode='rt', encoding='utf-8')
    else:
        return open(path, encoding='utf-8')


def parsed_entries(lines):
    for line in lines:
        yield line.split(' ', maxsplit=1)


def earlier():
    return (datetime.now() - timedelta(hours=24)).strftime('%d-%b-%y %H:%M:%S')


def get_files():
    return [LOGGER_PATH] + list(reversed(sorted(glob.glob(LOGGER_PATH))))


output = open(LOGS_24H_PATH, 'w', encoding='utf-8')


files = get_files()


cutoff = earlier()

def compress_24h_log():
        with open(LOGS_24H_PATH, 'rb') as source:
                content = source.read()
                with gzip.open(COMPRESSED_LOGS_24H_PATH, 'wb') as dest:
                        dest.write(content)
                        

def write_24h_log():
    for i, path in enumerate(files):
        with open_file(path) as f:
            lines = parsed_entries(f)
            # Assumes that your files are not empty
            date, line = next(lines)
            if cutoff <= date:
                # Skip files that can just be appended to the output later
                continue
            for date, line in lines:
                if cutoff <= date:
                    # We've reached the first entry of our file that should be
                    # included
                    output.write(line)
                    break
            # Copies from the current position to the end of the file
            shutil.copyfileobj(f, output)
            break
    else:
        # In case ALL the files are within the last 24 hours
        i = len(files)

    for path in reversed(files[:i]):
        with open_file(path) as f:
            # Assumes that your files have trailing newlines.
            shutil.copyfileobj(f, output)
    
    # Cleanup, it would get closed anyway when garbage collected or process exits.
    output.close()
    compress_24h_log()



def LOG_ERROR(logger:logging.Logger):
        e = sys.exc_info()
        logger.error("Exception: {0}".format(e))

def LOG_CONNECTION_ERROR(logger:logging.Logger):
        e = sys.exc_info()
        logger.error("SFTP connection failed")
        logger.error("Exception: {0}".format(e))

def LOG_DOWNLOAD_SUCCESFUL(logger:logging.Logger):
        logger.info("Download finished successfully")

def LOG_GET_ERROR(logger:logging.Logger, filename:str):
        e = sys.exc_info()
        logger.error("Error getting file "+ str(filename))
        logger.error("Exception: {0}".format(e))

def LOG_FILENOTLOCAL_INFO(logger, filename):
        logger.info("File "+str(filename)+" is not in backup folder and will be copied: ")

def LOG_LOCALFILEOVERWRITE_INFO(logger, filename):
        logger.info("Remote file "+str(filename)+" is bigger than local file, local file will be overwritten")

def LOG_START_PROGRAMM(logger:logging.Logger):
        logger.info("Start Programm")

def LOG_SAVING_COPIED_FILELIST(logger:logging.Logger):
        logger.info("Saving copied files")

def LOG_DOWNLOAD_INFO(logger:logging.Logger, filename:str, remotepath:str, localpath:str):
        logger.info("Downloading file "+str(filename) + " from remote: "+str(remotepath) + "To local: "+str(localpath))

def LOG_EXIT_INFO(logger:logging.Logger):
        logger.info("Exiting program")

def LOG_SENDMAIL_INFO(logger:logging.Logger):
        logger.info("Sending email")

