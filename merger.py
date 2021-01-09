import csv
import pandas as pd
from tkinter import messagebox


class Merger:
    dataframe = pd.DataFrame

    def isMergePossible(self, files: list):
        # TODO: also get header if there is none! and merge them if possible
        csvFiles = []
        xmlXslFiles = []

        # sort files
        for file in files:
            if file.endswith(".csv"):
                csvFiles.append(file)
            if file.endswith(".xml") or file.endswith(".xsl"):
                xmlXslFiles.append(file)

        #TODO: check if xml and csv can be merged

        isMatching = self.checkMatchingHeaderCSV(csvFiles)
        if isMatching is False:
            messagebox.showerror("Merge Error", "Cant merge tables without matching header columns!")

        return isMatching

    def mergeCSVFiles(self, files: list):
        mergedDf = pd.read_csv(files[0])
        print(mergedDf)
        for file in files[1:]:
            df = pd.read_csv(file)
            print(df)
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
