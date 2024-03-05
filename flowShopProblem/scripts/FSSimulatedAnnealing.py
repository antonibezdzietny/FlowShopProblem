import random
import numpy as np
from copy import copy 
from enum import IntEnum
from .FSDataFrame import FSDataFrame
from .FSUtilities import FSNeighborMoves, FSSummarizer


class FSSimulatedAnnealing:
    class SlopeFunctionType(IntEnum):
        GEOMETRIC = (0,)
        LOGARITHMIC = (1,)
        LINEAR = (2,)

    def __slopeGeometric(self, t0, tk, n, k):
        lmb = (np.finfo(float).eps / t0) ** (1 / n)
        return lmb * tk

    def __slopeLogarithmic(self,t0, tk, n, k):
        lmb = t0 / (n * t0 + np.finfo(float).eps)
        return tk / (1 + (lmb * tk))
    
    def __slopeLinear(self, t0, tk, n, k):
        return t0 / k


    def __init__(self, 
                 slopeFunctionType : SlopeFunctionType, 
                 moveNeighborMovesType : FSNeighborMoves.NeighborMovesTypes,
                 temperature_init : int = 1000,
                 max_iteration : int = 1000
                 ) -> None:
        # Select slope functions
        slopeFunctions = {0 : self.__slopeGeometric, 1 : self.__slopeLogarithmic, 2 : self.__slopeLinear}
        self._slopeFunction = slopeFunctions[slopeFunctionType]

        # Move type
        moveFunction = {0 : FSNeighborMoves.swap, 1 : FSNeighborMoves.reverseSubsequence, 2 : FSNeighborMoves.insertBefore, 3 : FSNeighborMoves.insertAfter}
        self._moveFunction = moveFunction[moveNeighborMovesType]

        # Copy other configuration 
        self._temperatureInit = temperature_init
        self._maxIteration    = max_iteration


    def __isAcceptableProbability(self):
        probability = np.min([ 1, np.exp( -(self._solutionCurrentP - self._solutionCurrent) / (self._temperatureCurrent + np.finfo(np.float32).eps) ) ])
        return random.random() < probability


    def __rollPositions(self):
        moves_index = np.arange(0, self._dataFrameBest.n_jobs, dtype=int)
        random.shuffle(moves_index)
        if self._slopeFunction in [FSNeighborMoves.swap, FSNeighborMoves.reverseSubsequence]:
            return np.sort(moves_index[0:2])
        return moves_index[0:2]


    def solve(self, dataFrame : FSDataFrame):
        # Copy structure for permutation
        self._dataFrameBest     = copy(dataFrame)
        self._dataFrameCurrent  = copy(dataFrame)
        self._dataFrameCurrentP = copy(dataFrame) 

        # Save solutions 
        self._solutionBest, _  = FSSummarizer.calculateCompletionTime(self._dataFrameBest)
        self._solutionCurrent  = self._solutionBest
        self._solutionCurrentP = self._solutionBest

        # Set current temperature 
        self._temperatureCurrent = self._temperatureInit 

        for i in range(1, self._maxIteration + 1):
            moves_index = self.__rollPositions()

            # Permutation new solution
            self._moveFunction(self._dataFrameCurrentP, moves_index[0], moves_index[1])
            self._solutionCurrentP, _  = FSSummarizer.calculateCompletionTime(self._dataFrameCurrentP)
            
            if self.__isAcceptableProbability():
                # If probability is acceptable copy current prime solution to prime solution
                self._dataFrameCurrent.tasks_index = self._dataFrameCurrentP.tasks_index.copy()
                self._solutionCurrent = self._solutionCurrentP

            
            if self._solutionCurrentP < self._solutionBest:
                # If checking solution is better than the best save it
                self._dataFrameBest.tasks_index = self._dataFrameCurrentP.tasks_index.copy()
                self._solutionBest = self._solutionCurrentP

            # Update current temperature
            self._temperatureCurrent = self._slopeFunction(self._temperatureInit, self._temperatureCurrent, self._maxIteration, i)

        # Return best solution
        return  self._dataFrameBest