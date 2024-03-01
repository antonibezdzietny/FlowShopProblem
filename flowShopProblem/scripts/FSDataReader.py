"""
Module implements data reader from .txt file in specific format
"""

from .FSDataFrame import FSDataFrame
import numpy as np
import os.path


class FSDataReader:
    """Public Method"""
    def __init__(self) -> None:
        self._path = ""
        self._n_tests = 0
        self._n_lines = 0
        self._ready_to_read = False


    def setPath(self, path : str):
        self._path = path
        self.__isCorrectPath()
        self.__isCorrectMinLength()
        

    """Private Method"""
    def __isCorrectPath(self):
        if not os.path.isfile(self._path):
            raise IOError("File not exist ...")
        

    def __isCorrectMinLength(self):
        if self._path == "":
            raise IOError("Set _path field ... ")
        
        self._n_lines = sum(1 for line in open(self._path, "r", encoding="UTF-8"))
        # Minimal file length is 4 lines
        if self._n_lines < 4:
            raise IOError("File .txt bad format")
        

    def __parseMetaConfig(self, data_frame : FSDataFrame, config_line : str):
        config = [int(conf) for conf in config_line.split()]
        data_frame.n_jobs        = config[0]
        data_frame.n_machines    = config[1]
        data_frame.init_seed     = config[2]
        data_frame.up_boundary   = config[3]
        data_frame.low_boundary  = config[4]


    def __parseData(self, data_frame : FSDataFrame, data_lines : list[str]):
        data_frame.processing_time = np.zeros((data_frame.n_machines, data_frame.n_jobs))

        for i, line in enumerate(data_lines):
            data_line = [int(x) for x in line.split()]
            data_frame.processing_time[i, :] = data_line


    def readData(self, n_set : int = 0) -> FSDataFrame:
        data_frame = FSDataFrame()   

        file = open(self._path, "r", encoding="UTF-8")
        
        # Skip to concrete set
        for i in range(0, n_set+1):
            file.readline() # Skip first line (its only comment to be more readable)
            config_line = file.readline()
            self.__parseMetaConfig(data_frame, config_line)

            file.readline() # Skip commentary line (its only comment to be more readable)
            data_lines = [file.readline() for _ in range(data_frame.n_machines)]
            if i == n_set:
                self.__parseData(data_frame, data_lines)
            
        file.close()

        return data_frame
   



