from src.pipeline import Pipeline, IElement
from pandas import DataFrame
import tempfile
from pathlib import Path
from typing import Iterable
from src.backup import backup, rollback
from line_profiler import profile
import uuid

class BackupManager:
    """ensure destination files are backuped and rollbacked in case of failure
    """
    def __init__(self, pipeline:Pipeline):
        self.pipeline=pipeline

    def __enter__(self):
        self.backup()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_tb:
            self.rollback()

    def backup(self)->None:
        [backup(p) for p in self.pipeline.files]
    
    def rollback(self)->None:
        [rollback(p) for p in self.pipeline.files]


class Executor():
    def __init__(self, pipeline:Pipeline) -> None:
        self._pipeline=pipeline
    
    async def run(self, source:DataFrame)->DataFrame:
        """init pipeline running and call elements sequence iteration

        Args:
            source (DataFrame): _description_

        Returns:
            DataFrame: _description_
        """
        run_id=uuid.uuid4()
        with tempfile.TemporaryDirectory() as tmp, BackupManager(self._pipeline) as bm:
            return await Executor._run_sequence(seq=self._pipeline.elements ,source=source)
    
    @staticmethod
    async def _run_sequence(seq:Iterable[IElement], source:DataFrame)->DataFrame:
        """runs the element sequence

        Args:
            source (DataFrame): _description_

        Returns:
            DataFrame: _description_
        """
        data=source

        for i, el in enumerate(seq):
            data = await Executor._run_element(el, data)
        
        return data
    
    @staticmethod
    async def _run_element(el:IElement, source:DataFrame)->DataFrame:
        try:
            return await el.run(source)
        except Exception as e:
            raise e

class ProfiledExecutor(Executor):
    @profile
    async def run(self, source: DataFrame) -> DataFrame:
        return await super().run(source)

EXECUTOR = Executor