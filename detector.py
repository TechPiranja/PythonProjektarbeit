import regex
import chardet
import csv
import pandas


def detectEncoding(filePath: str):
    with open(filePath, 'rb') as rawdata:
        result = chardet.detect(rawdata.read())
        return result["encoding"]


def hasHeader(filePath: str):
    with open(filePath, 'r') as rawdata:
        result = rawdata.read()
        return csv.Sniffer().has_header(result)


# guesses Header Names based on Type which is checked with Regex Match
def guessHeaderNames(dataFrame: pandas.DataFrame):
    headerNameCount = {}
    newHeaders = {}

    for column in dataFrame.columns:
        #get first data in column and detect its Type
        sampleFromColumn = str(dataFrame[column][0])
        headerName = regex.getHeaderName(sampleFromColumn)

        #add or increase count of Type
        if headerName not in headerNameCount:
            headerNameCount[headerName] = 0
        else:
            headerNameCount[headerName] += 1

        #concat headerName with count as new ColumnHeader
        newHeaders[column] = headerName + "_" + str(headerNameCount[headerName])
    return newHeaders
