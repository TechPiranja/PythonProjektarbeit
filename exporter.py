from pandastable import Table

def exportToCSV(filePath: str, pt: Table):
    pt.doExport(filePath)