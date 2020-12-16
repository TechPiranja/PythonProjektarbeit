import re

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


def guessHeaderNames(dataFrame: pandas.DataFrame):
    headerNames = {}
    newHeaderColumn = {}

    for column in dataFrame.columns:
        sample = str(dataFrame[column][0])
        headerName = getHeaderName(sample)

        if headerName not in headerNames:
            headerNames[headerName] = 0

        count = headerNames[headerName]
        headerName += "_" + str(count)

        #increment count for next usage
        headerNames[headerName] = count + 1
        newHeaderColumn[column] = headerName

    return newHeaderColumn


reEmail = re.compile(r"^[a-zA-Z0-9_.-]+@[a-zA-Z0-9.-]+.[a-z.]{2,6}$")
reDate = re.compile(r"^[0-3]?[0-9][/.][0-3]?[0-9][/.](?:[0-9]{2})?[0-9]{2}$")
reTime = re.compile(r"^[0-2]\d:[0-6]\d:[0-6]\d$")
reNumber = re.compile(r"^[+-]?\d+([,.]\d+)?$")
reCoordinate = re.compile(r"^(N|S)?0*\d{1,2}°0*\d{1,2}(′|')0*\d{1,2}\.\d*(″|\")(?(1)|(N|S)) (E|W)?0*\d{1,2}°0*\d{1,2}(′|')0*\d{1,2}\.\d*(″|\")(?(5)|(E|W))$")
reUrl = re.compile(r"^((ftp|http|https):\/\/)?(www.)?(?!.*(ftp|http|https|www.))[a-zA-Z0-9_-]+(\.[a-zA-Z]+)+((\/)[\w#]+)*(\/\w+\?[a-zA-Z0-9_]+=\w+(&[a-zA-Z0-9_]+=\w+)*)?$")


def getHeaderName(sample: str):
    if reEmail.match(sample):
        return "Email"

    if reDate.match(sample):
        return "Date"

    if reTime.match(sample):
        return "Time"

    if reNumber.match(sample):
        return "Number"

    if reCoordinate.match(sample):
        return "Coordinate"

    if reUrl.match(sample):
        return "Url"

    return "Text"
