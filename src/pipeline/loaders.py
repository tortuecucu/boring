from src.pipeline import IElement, Pipeline
from pathlib import Path
from typing import Optional
from abc import abstractclassmethod
from pandas import DataFrame

class ILoader(IElement):
    @abstractclassmethod
    async def run(self, source:DataFrame)->DataFrame:
        ...

class IFileLoader(ILoader):
    def __init__(self, path:Path, pipeline: 'Pipeline', step: int, level: Optional[int] = 1) -> None:
        super().__init__(path.name, pipeline, step, level)
        self._path=path
    
    @property
    def path(self)->Path:
        return self._path
