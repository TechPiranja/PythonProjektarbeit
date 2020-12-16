import pandas as pd


class Importer:
    dataFrame: pd.DataFrame

    def importCSV(self, file: str):
        # TODO: this is just for testing, delete this!
        self.dataFrame = pd.read_csv(file)

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
