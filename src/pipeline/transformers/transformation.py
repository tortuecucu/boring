from src.pipeline import IElement
from src.pipeline.transformers import ITransformer
from typing import Optional
from pandas import DataFrame
from pathlib import Path
from abc import abstractclassmethod

class ITransformation(IElement):
    def __init__(self, name: str, transformer:ITransformer, step: int, level: Optional[int] = 1) -> None:
        super().__init__(name, transformer.pipeline, step, level)
        self._transformer=transformer
    
    @property
    def transformer(self)->ITransformer:
        return self._transformer

    @abstractclassmethod
    async def run(self, source:DataFrame)->DataFrame:
        ...

class FileBackup(ITransformation):
    def __init__(self, path:Path, transformer: ITransformer, step: int, level: Optional[int] = 0) -> None:
        super().__init__(path.name, transformer, step, level)
        self._path=path
    
    async def run(self, source:DataFrame)->DataFrame:
        ...