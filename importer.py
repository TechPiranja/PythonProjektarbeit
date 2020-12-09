# the importer shall import csv files
import pandas as pd


class Importer:
    dataFrame: pd.DataFrame

    def importCSV(self):
        self.dataFrame = pd.read_csv(r'./testFiles/10000 Sales Records.csv')

    # def convertToList(self):
    #
    # def convertToNumArr(self):
    #
    def convertToPandasDF(self):
        print(self.dataFrame)
