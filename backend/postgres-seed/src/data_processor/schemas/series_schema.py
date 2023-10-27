"""
This module contains the SeriesSchema class for storing pandas Series data 
between services.
"""
import pandas as pd


class SeriesSchema:
    """
    A container for storing a named pandas Series object for
    inter-service data transfer.
    """

    def __init__(self, name: str, series: pd.Series):
        self.name = name
        self.series = series
