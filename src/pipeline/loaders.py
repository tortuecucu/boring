from src.pipeline import IElement, Pipeline
from pathlib import Path
from typing import Optional
from abc import abstractclassmethod
import pandas as pd

class ILoader(IElement):
    @abstractclassmethod
    async def run(self, source:pd.DataFrame)->pd.DataFrame:
        ...

class IFileLoader(ILoader):
    def __init__(self, path:Path, pipeline: 'Pipeline', step: int, level: Optional[int] = 1, parent:Optional[IElement]=None, name:Optional[str]=None, *args, **kwargs) -> None:
        super().__init__(pipeline=pipeline, step=step, level=level, parent=parent, name=name, args=args, kwargs=kwargs)
        self._path=path
    
    @property
    def path(self)->Path:
        return self._path


class CsvLoader(IFileLoader):
    async def run(self, source:pd.DataFrame)->pd.DataFrame:
        source.to_csv(
            path_or_buf=self.path,
            *self._args,
            **self._kwargs
        )
        return source

class ParquetLoader(IFileLoader):
    async def run(self, source:pd.DataFrame)->pd.DataFrame:
        source.to_parquet(
            path=self.path,
            *self._args,
            **self._kwargs
        )
        return source