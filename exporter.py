from lxml import etree
from tkinter import messagebox

def exportToCSV(filePath: str, dataframe, dialect):
    """
    Helper method which exports the dataframe from the importer_gui preview into a csv file with the given dialect.

    :param filePath: The file destination for the exported csv file
    :param dataframe: the dataframe from the importer_gui preview which will be converted into a csv file
    :param dialect: the dialect which will be used to convert the dataframe into a csv file
    """
    dataframe.to_csv(filePath + ".csv", encoding=dialect.encoding, sep=dialect.delimiter, quotechar=dialect.quoteChar, index=False)
    messagebox.showinfo(title="Success!", message="The Export was successful!")

def exportToXML(filePath: str, dataframe, encoding):
    """
    Helper method which export the dataframe from the importer_gui preview into a xml file with the given dialect.

    :param filePath: The file destination for the exported xml file
    :param dataframe: the dataframe from the importer_gui preview which will be converted into a xml file
    :param encoding: the encoding which will be used to convert the dataframe into a xml file
    """
    root = etree.Element('items')

    for i, row in dataframe.iterrows():
        item = etree.SubElement(root, 'item')

        for field in row.index:
            fieldElement = etree.SubElement(item, field)
            fieldElement.text = str(row[field])

    document = etree.ElementTree(root)
    document.write(filePath + ".xml", xml_declaration=True, pretty_print=True, encoding=encoding)
    messagebox.showinfo(title="Success!", message="The Export was successful!")
