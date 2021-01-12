from io import StringIO
import pandas as pd
import detector
from lxml import etree


class Importer:
    """
    The importer class is responsible for importing xml or csv files

    Attributes:
        dataFrame: the dataframe from the imported csv or xml
        dialect: the dialect from the imported file
    """
    dataFrame: pd.DataFrame
    dialect: detector.Dialect

    def importXML(self, xmlFile: str, xslFile: str):
        """
        converts the xml and xsl file into a csv and imports it

        :param xmlFile: the filepath to the xml file
        :param xslFile: the filepath to the xsl file
        """
        xmldoc = etree.parse(xmlFile)
        transformer = etree.XSLT(etree.parse(xslFile))
        result = str(transformer(xmldoc, param1=u"'value'"))
        data = StringIO(result)

        self.dialect = self.getXMLDialect(result)
        self.importCSV(data, self.dialect)

    def getXMLDialect(self, result):
        """
        guesses the dialect from the xml data

        :param result: the xml data
        :return: the guessed dialect from the xml data
        """
        dialect = detector.Dialect()
        dialect.guessDialectXML(result)
        return dialect

    def setDataFrame(self, df: pd.DataFrame):
        """
        helper method to set the dataframe from outside this class

        :param df: the dataframe which should override the dataframe of this class
        """
        self.dataFrame = df

    def importCSV(self, file: str, dialect: detector.Dialect):
        """
        imports a csv file or a buffer and saves it into the importer class dataframe attribute
        It also guesses HeaderNames if the dataframe hase none
        """
        self.dataFrame = pd.read_csv(file)

        if dialect.hasHeader is False:
            headers = detector.guessHeaderNames(self.dataFrame)
            self.dataFrame.rename(columns=headers, inplace=True)

    def getList(self):
        """
        :return: returns the imported dataframe to a list
        """
        return [list(self.dataFrame.columns), self.dataFrame.values.tolist()]

    def getDict(self):
        """
        :return: returns the imported dataframe to a dictionary
        """
        print(self.dataFrame.to_dict(orient="list"))

    def getNumpyArr(self):
        """
        :return: returns the imported dataframe to a numpy array
        """
        print(self.dataFrame.to_numpy())

    def getDataFrame(self):
        """
        :return: returns the imported dataframe
        """
        return self.dataFrame
