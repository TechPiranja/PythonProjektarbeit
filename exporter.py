from lxml import etree


def exportToCSV(filePath: str, dataframe, dialect):
    dataframe.to_csv(filePath + ".csv", encoding=dialect.encoding, sep=dialect.delimiter, quotechar=dialect.quotechar, index=False)
    #TODO: Message that the File was exported successfully!

def exportToXML(filePath: str, dataframe, dialect):
    root = etree.Element('items')

    for i, row in dataframe.iterrows():
        item = etree.SubElement(root, 'item')

        for field in row.index:
            fieldElement = etree.SubElement(item, field)
            fieldElement.text = str(row[field])

    document = etree.ElementTree(root)
    document.write(filePath + ".xml", xml_declaration=True, pretty_print=True, encoding=dialect.encoding)
