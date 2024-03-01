"""
Module implements data class for storing data in flow shop problem
"""

from dataclasses import dataclass, field
import numpy as np

@dataclass
class FSDataFrame:
    n_jobs       : int = 0
    n_machines   : int = 0
    init_seed    : int = 0
    up_boundary  : int = 0
    low_boundary : int = 0
    processing_time : np.ndarray = field(
        default_factory=lambda: np.zeros(shape=(int, int))  # type: ignore
    )

    def __init__(self) -> None:
        pass
