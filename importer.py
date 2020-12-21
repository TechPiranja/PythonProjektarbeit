from io import StringIO
import pandas as pd
import detector
from lxml import etree


class Importer:
    dataFrame: pd.DataFrame

    def importXML(self, xmlFile: str, xslFile: str):
        xmldoc = etree.parse(xmlFile)
        transformer = etree.XSLT(etree.parse(xslFile))

        # + Fehlerbehandlung: Datei-, Parsing-, Transformationsfehler
        result = str(transformer(xmldoc, param1=u"'value'"))
        data = StringIO(result)

        dialect = detector.Dialect()
        dialect.guessDialectXML(result)
        self.importCSV(data, dialect)
        return dialect

    def importCSV(self, file: str, dialect: detector.Dialect):
        # TODO: this is just for testing, delete this!
        self.dataFrame = pd.read_csv(file)

        #TODO: hasHeader has do be checked another way!
        if dialect.hasHeader is False:
           headers = detector.guessHeaderNames(self.dataFrame)
           self.dataFrame.rename(columns=headers, inplace=True)

    def getList(self):
        lists = self.dataFrame.values.tolist()
        header = list(self.dataFrame.columns)
        lists.insert(0, header)
        return lists

    def getDict(self):
        print(self.dataFrame.to_dict(orient="list"))

    def getNumpyArr(self):
        print(self.dataFrame.to_numpy())

    def getDataFrame(self):
        return self.dataFrame
