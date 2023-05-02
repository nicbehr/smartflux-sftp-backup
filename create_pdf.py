from datetime import datetime, timedelta, date
from typing import List
import pandas as pd
import os
import zipfile
from EC_data import EC_Data
import matplotlib.pyplot as plt
from paths import RAW_DATA_PATH, TEMPPATH
import re

format = '%Y-%m-%d %H:%M:%S:%f'

def parse_timestamp(filename):
    timestring_regex = re.compile('\d\d\d\d-\d\d-\d\dT\d\d\d\d\d\d')
    format = '%Y-%m-%dT%H%M%S'
    timestr_regex_result = timestring_regex.search(filename)
    if timestr_regex_result.group(0) is not None:
        timestr = timestr_regex_result.group(0)
        time = datetime.strptime(timestr,format)
        return time
    else:
        return datetime.now() - timedelta(hours=9999)

def get_last24h_filenames():
    oneDayBefore = datetime.now() - timedelta(hours=24)
    files = os.listdir()
    last_24h_filenames = []
    for root, dirs, files in os.walk(RAW_DATA_PATH):
        path = os.path.abspath(root)
        for file in files:
            time = parse_timestamp(file)
            if time > oneDayBefore:
                last_24h_filenames.append(os.path.join(path, file))
    return last_24h_filenames

def filter_last30days(files):
    today = date.today()
    todaymidnight = datetime.combine(today, datetime.min.time()) + timedelta(minutes=-30)
    before30days = todaymidnight - timedelta(days=30)
    indices = []
    for i,file in enumerate(files):
        time = parse_timestamp(str(file))
        if time > before30days:
            indices.append(i)
    last_30d_filenames = [files[i] for i in indices]
    return last_30d_filenames

def unzip_files(filelist):
    for file in filelist:
        if file not in os.listdir(TEMPPATH):
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall(TEMPPATH)


def get_last24h_data() -> EC_Data:
    last24h_files = get_last24h_filenames()
    last24h_files.sort()
    unzip_files(last24h_files)
    ec_data = EC_Data()
    ec_data.read_csvfiles(TEMPPATH)
    return ec_data

def get_last30day_filenames() -> list:
    filelist = []
    for root, dirs, files in os.walk(RAW_DATA_PATH):
        for file in files:
            #append the file name to the list
            if file.endswith('.ghg'):
                filelist.append(os.path.join(root,file))
    last30d_files = filter_last30days(filelist)
    return last30d_files

def get_files_and_filesizes(filenames):
    files_df = pd.DataFrame({
        "filename":pd.Series(dtype='str'),
        "size":pd.Series(dtype='int'),
        "timestamp":pd.Series(dtype='datetime64'),
    })

    for file in filenames:
        timestamp = pd.to_datetime(parse_timestamp(file))
        size = os.path.getsize(TEMPPATH + '/'+file)
        files_df = files_df.append({"filename":file, "size":size,"timestamp":timestamp})
    return files_df

def make_datelist() -> list():
    today = datetime.now().date()
    datelist = [today - timedelta(days=x) for x in range(31)]
    datelist.sort()
    return datelist

def make_timelist() -> list():
    today = datetime.now().date()
    midnight = datetime.min.time()
    todaymidnight = datetime.combine(today, midnight)
    timelist = [(todaymidnight + timedelta(minutes=x)).time() for x in range(0,1440,30)]
    return timelist

def make_file_df(filenames):
    datelist = make_datelist()
    timelist = make_timelist()

    df = pd.DataFrame(columns=datelist, index=timelist)
    
    for file in filenames:
        size = int(os.path.getsize(file))/1000
        date = parse_timestamp(file).date()
        time = parse_timestamp(file).time()
        if time not in df.index:
            times = df.index.tolist()
            times.append(time)
            times = times.sort()
            df = df.reindex(times)
        df[date][time] = size

    df = df.astype("float")
    for index in df.index:
        if not str(index).endswith(":00"):
            df = df.drop(index, axis=0)
    return df
