from src.pipeline import IElement
from abc import abstractclassmethod
import pandas as pd
from pathlib import Path
from typing import Optional

if True==False:
    from src.pipeline import Pipeline


class IExtractor(IElement):
    @abstractclassmethod
    async def run(self, source:Optional[pd.DataFrame]=None)->pd.DataFrame:
        ...

class IFileExtractor(IExtractor):
    def __init__(self, path:Path, pipeline: 'Pipeline', step: int, level: Optional[int] = 1, parent:Optional[IElement]=None, name:Optional[str]=None, *args, **kwargs) -> None:
        super().__init__(pipeline=pipeline, step=step, level=level, parent=None, name=None, args=args, kwargs=kwargs)
        self.path=path

class CsvExtractor(IFileExtractor):
    async def run(self, source:Optional[pd.DataFrame]=None)->pd.DataFrame:
        return pd.read_csv(
            filepath_or_buffer=self.path,
            *self._args,
            **self._kwargs
        ) #type: ignore
    
    @classmethod
    def element(cls, type:str, pipeline:Pipeline, step:int, level:Optional[int]=0, parent:Optional['IElement']=None, name:Optional[str]=None, *args, **kwargs)->'CsvExtractor':
        assert type=="CsvExtractor"
        assert "path" in kwargs
        return CsvExtractor(
            path=kwargs['path'],
            pipeline=pipeline,
            step=step,
            level=level,
            parent=parent,
            name=name,
            args=args,
            kwargs=kwargs
        )