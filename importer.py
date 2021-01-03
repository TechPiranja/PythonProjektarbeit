from io import StringIO
import pandas as pd
import detector
from lxml import etree


class Importer:
    dataFrame: pd.DataFrame
    dialect: detector.Dialect

    def importXML(self, xmlFile: str, xslFile: str):
        xmldoc = etree.parse(xmlFile)
        transformer = etree.XSLT(etree.parse(xslFile))

        # + Fehlerbehandlung: Datei-, Parsing-, Transformationsfehler
        result = str(transformer(xmldoc, param1=u"'value'"))
        data = StringIO(result)

        self.dialect = self.getXMLDialect(result)
        self.importCSV(data, self.dialect)

    def getXMLDialect(self, result):
        dialect = detector.Dialect()
        dialect.guessDialectXML(result)
        return dialect

    #used to set df from outside
    def setDataFrame(self, df: pd.DataFrame):
        self.dataFrame = df

    def importCSV(self, file: str, dialect: detector.Dialect):
        self.dataFrame = pd.read_csv(file)

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
