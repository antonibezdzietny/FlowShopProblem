from enum import IntEnum
from FSDataFrame import *



class FSNeighborMoves:
    class NeighborMovesTypes(IntEnum):
        """Type of available move in neighbor"""
        SWAP = (0,)
        REVERSE_SUBSEQUENCE = (1,)
        INSERT_BEFORE = (2,)
        INSERT_AFTER = (3,)

    @staticmethod
    def swap(data_frame : FSDataFrame, index_1 : int, index_2 : int):
        data_frame[:, [index_1, index_2]] = data_frame[:, [index_2, index_1]]

    @staticmethod
    def reverse_subsequence(data_frame : FSDataFrame, start : int, end : int ):
        data_frame[:, start : end+1] = data_frame[:, start : end+1][::-1]

    @staticmethod
    def insert_before(data_frame : FSDataFrame, index_1 : int, index_2 : int):
        buff = data_frame[:, index_1]

        if index_1 < index_2:
            data_frame[:, index_1 : index_2] = data_frame[:, index_1 + 1 : index_2 + 1]
            data_frame[:, index_2 - 1] = buff
        elif index_1 > index_2:
            data_frame[:, index_1 + 1 : index_2 + 1] = data_frame[:, index_1 : index_2]
            data_frame[:, index_2] = buff
    
    @staticmethod
    def insert_after(data_frame : FSDataFrame, index_1 : int, index_2 : int):
        buff = data_frame[:, index_1]

        if index_1 < index_2:
            data_frame[:, index_1 : index_2] = data_frame[:, index_1 + 1 : index_2 + 1]
            data_frame[:, index_2] = buff
        elif index_1 > index_2:
            data_frame[:, index_2 + 1 : index_1 + 1] = data_frame[:, index_2 : index_1]
            data_frame[:, index_2 + 1] = buff