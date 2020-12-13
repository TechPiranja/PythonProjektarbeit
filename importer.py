# the importer shall import csv files
import pandas as pd


class Importer:
    dataFrame: pd.DataFrame

    def importCSV(self, file: str):
        # TODO: this is just for testing, delete this!
        self.dataFrame = pd.read_csv(file)

    # def convertToList(self):
    #

    def getDict(self):
        print(self.dataFrame.to_dict())

    def getNumpyArr(self):
        print(self.dataFrame.to_numpy())

    def getDataFrame(self):
        return self.dataFrame