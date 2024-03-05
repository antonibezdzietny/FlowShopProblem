import random
import numpy as np
from enum import IntEnum
import matplotlib.pyplot as plt
from .FSDataFrame import FSDataFrame
from matplotlib.patches import Rectangle



class FSNeighborMoves:
    class NeighborMovesTypes(IntEnum):
        """Type of available move in neighbor"""
        SWAP = (0,)
        REVERSE_SUBSEQUENCE = (1,)
        INSERT_BEFORE = (2,)
        INSERT_AFTER = (3,)

    @staticmethod
    def swap(data_frame : FSDataFrame, index_1 : int, index_2 : int):
        data_frame.tasks_index[[index_1, index_2]] = data_frame.tasks_index[[index_2, index_1]]
    
    @staticmethod
    def reverseSubsequence(data_frame : FSDataFrame, start : int, end : int ):
        data_frame.tasks_index[start : end+1] = data_frame.tasks_index[start : end+1][::-1]

    @staticmethod
    def insertBefore(data_frame : FSDataFrame, index_1 : int, index_2 : int):
        buff = data_frame.tasks_index[index_1]

        if index_1 < index_2:
            data_frame.tasks_index[index_1 : index_2] = data_frame.tasks_index[index_1 + 1 : index_2 + 1]
            data_frame.tasks_index[index_2 - 1] = buff
        elif index_1 > index_2:
            data_frame.tasks_index[index_1 + 1 : index_2 + 1] = data_frame.tasks_index[index_1 : index_2]
            data_frame.tasks_index[index_2] = buff
    
    @staticmethod
    def insertAfter(data_frame : FSDataFrame, index_1 : int, index_2 : int):
        buff = data_frame.tasks_index[index_1]

        if index_1 < index_2:
            data_frame.tasks_index[index_1 : index_2] = data_frame.tasks_index[index_1 + 1 : index_2 + 1]
            data_frame.tasks_index[index_2] = buff
        elif index_1 > index_2:
            data_frame.tasks_index[index_2 + 1 : index_1 + 1] = data_frame.tasks_index[index_2 : index_1]
            data_frame.tasks_index[index_2 + 1] = buff


class FSSummarizer:
    @staticmethod
    def calculateCompletionTime(data_frame : FSDataFrame):
        completion_array = np.zeros((data_frame.n_machines, data_frame.n_jobs))

        # Fill first column
        for i in range(data_frame.n_machines):
            completion_array[i][0] = data_frame.processing_time[i][data_frame.tasks_index[0]] + completion_array[i-1][0]

        #Fill first row
        for i in range(1, data_frame.n_jobs):
            completion_array[0][i] = data_frame.processing_time[0][data_frame.tasks_index[i]] + completion_array[0][i-1]
        
        #Fill array for next tasks
        for i in range(1, data_frame.n_machines):
            for j in range(1, data_frame.n_jobs):
                completion_array[i][j] = np.max((completion_array[i-1][j], completion_array[i][j-1])) + data_frame.processing_time[i][data_frame.tasks_index[j]]
        
        return completion_array[-1][-1], completion_array 
    

    @staticmethod
    def displayGraph(data_frame : FSDataFrame, completion_array):
        plt.figure()
        axis = plt.gca()

        # Colors picker 
        colors = plt.cm.tab20(np.linspace(0, 1, data_frame.n_jobs))

        # Display job diagram
        for i, machine in enumerate(completion_array):
            size_y = 0.9
            pos_y_box = i - size_y / 2 + 1

            for j, task in enumerate(machine):
                size_x = data_frame.processing_time[i][data_frame.tasks_index[j]]
                pos_x_box = task - size_x
                axis.add_patch(
                Rectangle(
                    (pos_x_box, pos_y_box),
                    size_x,
                    size_y,
                    facecolor=colors[data_frame.tasks_index[j]],
                    alpha=0.9,
                    linewidth=0.4,
                    edgecolor="k",
                )
            )
        plt.title("Flow Shop Problem")
        plt.xlabel("Time")
        plt.ylabel("Machines")
        plt.yticks(range(1, data_frame.n_machines + 1))
        plt.xlim([0, completion_array[-1][-1]])
        plt.ylim([0, data_frame.n_machines + 1])
        plt.ylim([0, data_frame.n_machines + 1])
        plt.show()