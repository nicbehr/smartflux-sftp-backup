
import logging
import pandas as pd
import os 

format = '%Y-%m-%d %H:%M:%S:%f'

# instantiate logger
logger = logging.getLogger(__name__)

class EC_Data():
    
    def __init__(self):
        self.data = pd.DataFrame()
        self.units = pd.DataFrame()

    def read_csvfiles(self, path):
        fileList = []
        biomet_filelist = []
        
        logger.info("Started searching data in "+path)
        for path, subdirs, files in os.walk(path):
            for name in files:
                if(name.endswith("-biomet.data")):
                    biomet_filelist.append(path + "/" + name)
                elif(name.endswith(".data") ):
                    fileList.append(path + "/" + name)
        fileList.sort()
        biomet_filelist.sort()
        logger.info("finished searching")
        logger.info("found " + str(len(fileList))+ " files.")
        logger.info("found " + str(len(biomet_filelist))+ " biomet files.")

        logger.info("Concatenating data")
        self.data = pd.concat([pd.read_csv(name, sep="\t", header=1, skiprows=6, parse_dates=[['Date', 'Time']]) for name in fileList])       
        logger.info("Extracting units")
        self.units = pd.read_csv(fileList[0], sep=",", header=1, nrows=1,skiprows=5) 

        logger.info("Reading biomet data")
        biomet_data = pd.concat([pd.read_csv(name, sep="\t", skiprows=5, parse_dates=[['DATE', 'TIME']]) for name in biomet_filelist]) 
        biomet_data = biomet_data.rename(columns={"DATE_TIME":"Date_Time"})
        #biomet_units = pd.read_csv(biomet_filelist[0], sep=",", nrows=1, skiprows=4)
        self.data = pd.merge(self.data, biomet_data, on="Date_Time")
        #self.units.merge(biomet_units, how="outer")
        #self.data["SWIN_1_1_1"][self.data["SWIN_1_1_1"] < 0] = 0
        logger.info("Finished reading biomet data")
        self.data.index = self.data["Date_Time"]
        self.data.index = pd.to_datetime(self.data.index, format=format)