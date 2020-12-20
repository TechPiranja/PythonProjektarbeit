from pandastable import Table

def exportToCSV(pt: Table):
    pt.doExport("./testFiles/testfile1.csv")
    print("Test1")