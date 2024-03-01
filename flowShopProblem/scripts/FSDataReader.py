"""
Module implements data reader from .txt file in specific format
"""

from .FSDataFrame import FSDataFrame
import os.path


class FSDataReader:
    """Public Method"""
    def __init__(self) -> None:
        self._path = ""
        self._n_tests = 0

    def setPath(self, path : str):
        self._path = path
        self._isCorrectPath()


    """Private Method"""
    def _isCorrectPath(self):
        if not os.path.isfile(self._path):
            raise Exception("File not exist ...")



    def readData(self, n_set : int = 0) -> FSDataFrame:
        dataFrame = FSDataFrame()   
        pass


