# the importer shall import csv files
import pandas as pd


class Importer:
    dataFrame: pd.DataFrame

    def importCSV(self):
        # TODO: this is just for testing, delete this!
        self.dataFrame = pd.read_csv(r'./testFiles/10000 Sales Records.csv')

    # def convertToList(self):
    #

    def getDict(self):
        print(self.dataFrame.to_dict())

    def getNumpyArr(self):
        print(self.dataFrame.to_numpy())

    def getDataFrame(self):
        print(self.dataFrame)