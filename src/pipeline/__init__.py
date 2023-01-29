from ctypes import Union
from functools import cache
from typing import Callable, Iterable, Iterator, Optional, Set, Dict, List, Type
from abc import ABC, abstractclassmethod
from pandas import DataFrame
from src.pipeline.schema import Schema
from pathlib import Path
import weakref
import asyncio
from random import randint

class Pipeline():
    def __init__(self, schema:Schema) -> None:
        self._schema=schema
        self._elements=[]

    @property
    def name(self)->str:
        return self._schema.name
    
    @property
    def schema(self)->Schema:
        return self._schema
    
    @property
    def elements(self)->List['IElement']:
        return self._elements

    def find_elements(self, filter:Callable, base:Optional[Iterable['IElement']]=None)->Iterator['IElement']:
        from src.pipeline.groups import IGroup, SubPipeline
        base=base if base else self.elements
        for e in base:
            if filter(e): yield e
            if isinstance(e, IGroup):
                yield from self.find_elements(filter, e.elements)
                
    @property
    def extractors(self)->'IExtractor': #type: ignore
        from src.pipeline.extractors import IExtractor
        return {e for e in self.find_elements(filter=lambda x: isinstance(x, IExtractor))}
    
    @property
    def loaders(self)->Set['ILoader']: #type: ignore
        from src.pipeline.loaders import ILoader
        return {e for e in self.find_elements(filter=lambda x: isinstance(x, ILoader))}
    
    @property
    def files(self)->Set[Path]:
        from src.pipeline.loaders import IFileLoader
        return {l.path for l in self.loaders if isinstance(l, IFileLoader)}

    async def run(self, source:DataFrame)->DataFrame:
        from src.pipeline.executor import EXECUTOR as Ex
        return await Ex(self).run(source=source)

    
    @classmethod
    def pipeline(cls, name:str)->'Pipeline':
        return Pipeline(schema=Schema.schema(name))


class IElement(ABC):
    _instances:Set=set()
    _counter:int=0
    def __init__(self, pipeline:'Pipeline', step:int, level:Optional[int]=0, parent:Optional['IElement']=None, name:Optional[str]=None, *args, **kwargs) -> None:
        self._counter+=1
        self._name=name if name else f"Element #{self._counter} <{self.__class__.__name__}>"
        self._step=step
        self._level=level
        self._pipeline=pipeline
        self._args=args
        self._kwargs=kwargs
        
    def __del__(self)->None:
        IElement._instances.remove(self)
    
    @property
    def step(self)->int:
        return self._step
    @property
    def level(self)->int:
        return self._level  # type: ignore
    @property
    def pipeline(self)->'Pipeline':
        return self._pipeline
    @property
    def name(self)->str:
        return self._name  # type: ignore
    
    @abstractclassmethod
    async def run(self, source:DataFrame)->DataFrame: # type: ignore 
        pass
    
    @classmethod
    def types(cls):
        @cache
        def walker():
            return IElement.all_subclasses(cls)
        return walker()

    @staticmethod    
    def all_subclasses(class_type):
        return set(class_type.__subclasses__()).union(
            [s for c in class_type.__subclasses__() for s in IElement.all_subclasses(c)])

    @classmethod
    def element(cls, type:str, pipeline:Pipeline, step:int, level:Optional[int]=0, parent:Optional['IElement']=None, name:Optional[str]=None, *args, **kwargs)->'IElement':
        from src.pipeline.extractors import IFileExtractor
        
        @cache
        def get_class(class_name:str):
            matches = [t for t in cls.types() if t.__name__==class_name]
            return matches[0] if len(matches)>0 else None
        
        named_args = {
            'pipeline': pipeline,
            'step': step,
            'level': level,
            'parent': parent,
            'name': name
        }
        if kwargs:named_args.update(kwargs)
        
        return get_class(type).element(*args, **named_args) #type: ignore

class PipelineFactory():
    @staticmethod
    def pipeline(schema:Schema)->Pipeline:
        step=0
        pipe=Pipeline(schema=schema)

        def _element(el:Dict)->None:
            nonlocal step
            pipe._elements.append(
                 IElement.element(
                    *el.get('args',[]),
                    type=el.get('class'),  # type: ignore
                    pipeline=pipe,
                    step=step,
                    name=el.get('name'),
                    **el.get('kwargs',dict())
                )
            )
            step+=1
        
        [_element(e) for e in schema._data.get('elements')]
        return pipe
        
class FakeElement(IElement):
    def __init__(self, pipeline: 'Pipeline', step: int, level: Optional[int] = 0, parent: Optional['IElement'] = None, name: Optional[str] = None) -> None:
        super().__init__(pipeline, step, level, parent, name)
    
    async def run(self, source:DataFrame)->DataFrame:
        await asyncio.sleep(randint(1,3))
        return source

class DeepFake(FakeElement):
    pass