import csv
import pandas as pd
from tkinter import messagebox
from importer import Importer


class Merger:
    """
    The Merger class can convert files into CSV to prepare them before merging. It can merge multiple CSV and XML/XSL Files.
    Its also responsible for checking the headers before merging on compatibility.

    Attributes:
        importer    importer object which is also used by the importer_gui (single instance)
        csvFiles    the csvFile, List which is created in the prepareMerge method, is saved to use it later in the mergeFiles method
        xmlList     the xmlList, which is created in the prepareMerge method, is saved to use it later in the mergeFiles method
    """
    importer = Importer
    csvFiles = []
    xmlList = []

    def __init__(self, importer: Importer):
        """
        The init method of the Merger is importent in order to get the same importer instance (singelton)

        :param importer: the importer object which is also used by the importer_gui
        """
        self.importer = importer

    def convertToCSV(self, xmlFile, xslFile):
        """
        This is a helper method to convert xml and xsl file into a csv in order to merge it correctly

        :param xmlFile: xmlFile to convert
        :param xslFile: xslFile to convert
        :return: converted csv file
        """
        self.importer.importXML(xmlFile, xslFile)

    def prepareMerge(self, files: list, xmlList: list):
        """
        Helper method to prepare a list before merging. It sorts the files so we can identify csv from xml/xsl.
        After that, the headers of all files are checked for matching headers.

        :param files: the imported file list from the importer_gui
        :param xmlList: the xml List which contains its corresponding xsl file
        :return: boolean if the headers of the given files are matching and allowed to be merged
        """
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
        """
        This is the Main method of this class. It uses the prepared csv and xml list and merges them with the helper methods.
        After merging it clears those lists for the next preparement and merging process.

        :return: The merged dataframe from the prepared csv and xml list
        """
        mergedDf = pd.DataFrame
        if len(self.csvFiles) > 0 and len(self.xmlList) > 0:
            mergedCSVDf = self.mergeCSVFiles(self.csvFiles)
            mergedXMLDf = self.mergeXMLList(self.xmlList)
            mergedDf = pd.concat([mergedCSVDf, mergedXMLDf])
        elif len(self.csvFiles) > 0:
            mergedDf = self.mergeCSVFiles(self.csvFiles)
        elif len(self.xmlList) > 0:
            mergedDf = self.mergeXMLList(self.xmlList)

        #clears the prepared sorted lists
        self.xmlList = []
        self.csvFiles = []

        return mergedDf

    def mergeCSVFiles(self, files: list):
        """
        converts all the files inside the fileslist into CSV and then merges them into one single dataframe

        :param files: files which will be converted to CSV and merged
        :return: returns merged dataFrame out of the CSV files
        """
        mergedDf = pd.read_csv(files[0])
        for file in files[1:]:
            df = pd.read_csv(file)
            mergedDf = pd.concat([mergedDf, df])
        return mergedDf

    def mergeXMLList(self, xmlList: list):
        """
        This method it only for merging xml files. It converts each file into an csv before concatenating it into a dataframe

        :param xmlList: the xml list which will be merged into a dataframe
        :return: the merged dataframe
        """
        self.convertToCSV(xmlList[0][0], xmlList[0][1])
        mergedDf = self.importer.getDataFrame()
        for valuePair in xmlList[1:]:
            self.convertToCSV(valuePair[0], valuePair[1])
            df = self.importer.getDataFrame()
            mergedDf = pd.concat([mergedDf, df])
        return mergedDf

    def checkMatchingHeaderCSV(self, files: list):
        """
        Checks if the headers of all given files are matching

        :param files: the fileslist which will be checked
        :return: boolean if the headers are matching or not
        """
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
