import regex
import chardet
import csv
import pandas


class Dialect:
    encoding: str = "utf-8"
    hasHeader: bool = False
    delimiter: str = ","
    quoteChar: str = "\""

    def guessDialectCSV(self, filePath: str):
        self.encoding = self.detectEncoding(filePath)

        with open(filePath, 'r') as rawdata:
            data = rawdata.read()
            self.hasHeader = self.hasHeader(data)
            self.quotechar = self.getSniffer(data).quotechar
            self.delimiter = self.getSniffer(data).delimiter

    def guessDialectFromData(self, data: str):
        self.quotechar = self.getSniffer(data).quotechar
        self.delimiter = self.getSniffer(data).delimiter
        self.hasHeader = self.hasHeader(data)

    def detectEncoding(self, filePath: str):
        with open(filePath, 'rb') as rawdata:
            data = rawdata.read()
        result = chardet.detect(data)
        return result["encoding"]

    def hasHeader(self, data: str):
        return csv.Sniffer().has_header(data)

    def getSniffer(self, data: str):
        return csv.Sniffer().sniff(data)


# guesses Header Names based on Type which is checked with Regex Match
def guessHeaderNames(dataFrame: pandas.DataFrame):
    headerNameCount = {}
    newHeaders = {}

    for column in dataFrame.columns:
        # get first data in column and detect its Type
        sampleFromColumn = str(dataFrame[column][0])
        headerName = regex.getHeaderName(sampleFromColumn)

        # add or increase count of Type
        if headerName not in headerNameCount:
            headerNameCount[headerName] = 0
        else:
            headerNameCount[headerName] += 1

        # concat headerName with count as new ColumnHeader
        newHeaders[column] = headerName + "_" + str(headerNameCount[headerName])
    return newHeaders
