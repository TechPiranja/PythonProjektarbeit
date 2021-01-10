import csv
import pandas as pd
from tkinter import messagebox

from importer import Importer


class Merger:
    dataframe = pd.DataFrame
    importer = Importer
    csvFiles = []
    xmlList = []

    def __init__(self, importer: Importer):
        self.importer = importer

    def convertToCSV(self, xmlFile, xslFile):
        self.importer.importXML(xmlFile, xslFile)

    def prepareMerge(self, files: list, xmlList: list):
        # TODO: also get header if there is none! and merge them if possible
        self.xmlList = xmlList

        # sort files
        for file in files:
            if file.endswith(".csv"):
                self.csvFiles.append(file)

        #TODO: check if xml and csv can be merged

        isMatching = self.checkMatchingHeaderCSV(self.csvFiles)
        if isMatching is False:
            messagebox.showerror("Merge Error", "Cant merge tables without matching header columns!")

        return isMatching

    def mergeFiles(self):
        mergedDf = pd.DataFrame
        if len(self.csvFiles) > 0 and len(self.xmlList) > 0:
            mergedCSVDf = self.mergeCSVFiles(self.csvFiles)
            mergedXMLDf = self.mergeXMLList(self.xmlList)
            mergedDf = pd.concat([mergedCSVDf, mergedXMLDf])
        elif len(self.csvFiles) > 0:
            mergedDf = self.mergeCSVFiles(self.csvFiles)
        elif len(self.xmlList) > 0:
            mergedDf = self.mergeXMLList(self.xmlList)

        #clear sorted list
        self.xmlList = []
        self.csvFiles = []

        return mergedDf

    def mergeCSVFiles(self, files: list):
        mergedDf = pd.read_csv(files[0])
        for file in files[1:]:
            df = pd.read_csv(file)
            mergedDf = pd.concat([mergedDf, df])
        return mergedDf

    def mergeXMLList(self, xmlList: list):
        self.convertToCSV(xmlList[0][0], xmlList[0][1])
        mergedDf = self.importer.getDataFrame()
        for valuePair in xmlList[1:]:
            self.convertToCSV(valuePair[0], valuePair[1])
            df = self.importer.getDataFrame()
            mergedDf = pd.concat([mergedDf, df])
        return mergedDf

    def checkMatchingHeaderCSV(self, files: list):
        checkHeader = []
        for file in files:
            with open(file, "r") as f:
                reader = csv.reader(f)
                header = next(reader)

                if not checkHeader:
                    checkHeader = header
                    continue

                # if the Header is not matching return False
                if set(header) != set(checkHeader):
                    print(header)
                    print(checkHeader)
                    return False

        return True
