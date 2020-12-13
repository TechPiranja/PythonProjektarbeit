import chardet
import csv

def detectEncoding(filePath: str):
    with open(filePath, 'rb') as rawdata:
        result = chardet.detect(rawdata.read())
        return result["encoding"]

def detectHeader(filePath: str):
    with open(filePath, 'r') as rawdata:
        result = rawdata.read()
        return csv.Sniffer().has_header(result)
