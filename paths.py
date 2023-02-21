import os
filepath = os.path.abspath(__file__)
wd = os.path.dirname(filepath)

REMOTE_DATA_PATH = './data/'
DATA_PATH = wd + '/data/'
CNOPTS_LOG_PATH = wd + '/logs/sftp_log.txt'
KNOWN_HOSTS_PATH = wd + '/static/known_hosts'
COPIED_FILES_PATH = wd + '/logs/copied_files/'
LOGGER_PATH = wd + "/logs/logger.log"
LOGS_24H_PATH = wd + '/logs/log_24h.log'
LOGS_PATH = wd + '/logs/'
COMPRESSED_LOGS_24H_PATH = wd + '/logs/log_24h.log.gz'
FIGUREPATH = wd + '/figures'
TEMPPATH = wd + '/temp'
RAW_DATA_PATH = wd + '/data/raw'