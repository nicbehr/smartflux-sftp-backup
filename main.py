# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 09:43:55 2022

@author: Nicolas Behrens
"""

import logging
from create_pdf import get_last24h_data, get_last30day_filenames, make_file_df
import sftp_runner
import misc_util
import logging.handlers as handlers
import emailer
import logging_util as l
from datetime import datetime
from paths import LOGGER_PATH, RAW_DATA_PATH
import plots as p
import sys 

DATEFORMAT = '%d-%b-%y %H:%M:%S'

#--- not implemented
#logHandler = handlers.TimedRotatingFileHandler('./logs/logger.log', when='D', interval=1)
#logger.addHandler(logHandler)

debug = True

if debug == False:
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt=DATEFORMAT, level=logging.INFO, filename=LOGGER_PATH)
else:
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt=DATEFORMAT, level=logging.INFO, stream=sys.stdout)

logger = logging.getLogger(__name__)


def run_backup():

    l.LOG_START_PROGRAMM(logger)
    copied_files = sftp_runner.start_process()
    l.LOG_SAVING_COPIED_FILELIST(logger)
    copied_files_file = misc_util.write_copied_files(copied_files=copied_files)
    l.write_24h_log()
    l.LOG_EXIT_INFO(logger)

def send_email(endtime, timedelta):
    l.LOG_SENDMAIL_INFO(logger)
    emailer.send_email(endtime, timedelta)

def make_plots():
    ghg_filenames_30days = get_last30day_filenames()
    ghg_filenames_30days.sort()
    df = make_file_df(ghg_filenames_30days)

    ec_data_24h = get_last24h_data()
    p.make_plot_pdf(ec_data_24h, df)
    misc_util.clean_temp_folder()

def main():
    starttime = datetime.now()
    run_backup()
    make_plots()
    endtime = datetime.now()
    timedelta = str(endtime-starttime)
    send_email(endtime, timedelta)

if __name__ == '__main__':
    main()