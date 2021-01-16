import regex
import chardet
import csv
import pandas


class Dialect:
    """
    The Dialect class can guess the dialect from a csv or xml file. It is also able to detect the Encoding of a file,
    check its header, and fill the header with correct header names if there is none.

    Attributes:
        encoding: pre-defined default encoding
        hasHeader: pre-defined default hasHeader
        delimiter: pre-defined default delimiter
        quoteChar: pre-defined default quoteChar
    """
    encoding: str = "utf-8"
    hasHeader: bool = False
    delimiter: str = ","
    quoteChar: str = "\""

    def guessDialectCSV(self, filePath: str):
        """
        This method guesses the dialect from a csv file

        :param filePath: the csv filepath which will be sniffed in order to get the dialect data
        """
        self.encoding = self.detectEncoding(filePath)

        with open(filePath, 'r') as rawdata:
            data = rawdata.read()
            self.hasHeader = self.checkHasHeader(data)
            self.quotechar = self.getSniffer(data).quotechar
            self.delimiter = self.getSniffer(data).delimiter

    def guessDialectXML(self, data: str):
        """
        This method guesses the dialect from a xml file

        :param data: the data from the read etree.pass method
        """
        self.encoding = "utf-8"
        self.quotechar = self.getSniffer(data).quotechar
        self.delimiter = self.getSniffer(data).delimiter
        self.hasHeader = self.checkHasHeader(data)

    def detectEncoding(self, filePath: str):
        """
        Detect the encoding of the given file

        :param filePath: the given filepath which will be used to detec the encoding
        :return: the detected encoding of the file
        """
        with open(filePath, 'rb') as rawdata:
            data = rawdata.read()
        result = chardet.detect(data)
        return result["encoding"]

    def checkHasHeader(self, data: str):
        """
        Uses the csv sniffer to detect if the given data contains a header

        :param data: the data which is read from the rawdata.read
        :return: boolean if the data contains a header
        """
        return csv.Sniffer().has_header(data)

    def getSniffer(self, data: str):
        """
        gets the sniffer from the csv sniffer from the given data

        :param data: the data which is read from the rawdata.read
        :return: the csv sniffer from the given data
        """
        return csv.Sniffer().sniff(data)


def guessHeaderNames(dataFrame: pandas.DataFrame):
    """
    guesses header names based on the types in each column which is then checked with regex match

    :param dataFrame: the dataframe from the importer_gui
    :return: the new header column
    """
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
