from typing import Optional, Set, Dict, List
from abc import ABC, abstractclassmethod
from pandas import DataFrame
from src.pipeline.schema import Schema
from pathlib import Path
import weakref

class Pipeline():
    def __init__(self, schema:Schema, path:Path, elements:Set['IElement']) -> None:
        self._shema=schema
        self._destination=path
        self._elements=elements
        self._temp:Path=None

    @property
    def name(self)->str:
        ...
    
    @property
    def schema(self)->Schema:
        return self._shema

    @property
    def destination(self)->Path:
        return self._destination

    @property
    def temp(self)->Path:
        return self._temp
    
    @property
    def elements(self)->Set['IElement']:
        return self._elements

    @property
    def extractor(self)->'IExtractor': #type: ignore
        ...
    
    @property
    def loaders(self)->Set['ILoader']: #type: ignore
        ...


class IElement(ABC):
    _instances:Dict['Pipeline', List['IElement']]
    def __init__(self, name:str, pipeline:'Pipeline', step:int, level:Optional[int]=1) -> None:
        self._name=name
        self._step=step
        self._level=level
        self._pipeline=pipeline
        if not pipeline in self._instances:
            self._instances[pipeline]
        self._instances[pipeline].append(weakref.ref(self))

    @property
    def step(self)->int:
        return self._step
    @property
    def level(self)->int:
        return self._level
    @property
    def pipeline(self)->'Pipeline':
        return self._pipeline
    @property
    def name(self)->str:
        return self._name
    
    @abstractclassmethod
    async def run(self, source:DataFrame)->DataFrame:
        pass

class PipelineFactory():
    @staticmethod
    def pipeline(schema:Schema)->Pipeline:
        ...

class Executor():
    def __init__(self, pipeline:Pipeline) -> None:
        self._pipeline=pipeline
    
    async def run(self)->DataFrame:
        ...