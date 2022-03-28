import abc
import os
import json

from tqdm import tqdm

from . import util

class Dataset(abc.ABC):
    @abc.abstractmethod
    def name(self):
        """
        Returns the name of the dataset
        """
        pass

    @abc.abstractmethod
    def download(self):
        """
        Downloads the dataset
        """
        pass

    @abc.abstractmethod
    def clean(self):
        """
        Cleans the dataset
        """
        pass

    @abc.abstractmethod
    def size(self):
        """
        Returns the size of the dataset
        """
        pass
