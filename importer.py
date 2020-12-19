from io import StringIO
import pandas as pd
import detector
from lxml import etree


class Importer:
    dataFrame: pd.DataFrame

    def importXML(self):
        xmldoc = etree.parse("./testFiles/cdcatalog.xml")
        transformer = etree.XSLT(etree.parse("./testFiles/cdcatalog2csv.xsl"))
        # + Fehlerbehandlung: Datei-, Parsing-, Transformationsfehler
        result = str(transformer(xmldoc, param1=u"'value'"))
        data = StringIO(result)
        self.importCSV(data)

    def importCSV(self, file: str):
        # TODO: this is just for testing, delete this!
        self.dataFrame = pd.read_csv(file)

        #TODO: hasHeader has do be checked another way!
        #if detector.hasHeader(file) is False:
        #    headers = detector.guessHeaderNames(self.dataFrame)
        #    self.dataFrame.rename(columns=headers, inplace=True)

    def getList(self):
        lists = self.dataFrame.values.tolist()
        header = list(self.dataFrame.columns)
        lists.insert(0, header)
        return lists

    def getDict(self):
        print(self.dataFrame.to_dict(orient="list"))

    def getNumpyArr(self):  # TODO: only accept number tables!
        print(self.dataFrame.to_numpy(dtype="float32"))

    def getDataFrame(self):
        return self.dataFrame
