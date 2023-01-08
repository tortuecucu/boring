from src.pipeline import IElement
from abc import abstractclassmethod
from pandas import DataFrame
from pathlib import Path
from typing import Optional

if True==False:
    from src.pipeline import Pipeline


class IExtractor(IElement):
    @abstractclassmethod
    async def run(self, source:None=None)->DataFrame:
        ...

class IFileExtractor(IExtractor):
    def __init__(self, path:Path, pipeline: 'Pipeline', step: int, level: Optional[int] = 1) -> None:
        super().__init__(path.name, pipeline, step, level)
        self.path=path