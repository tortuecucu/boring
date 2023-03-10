from src.pipeline import IElement, Pipeline
from collections import UserList
from typing import Optional, List, Iterator, Coroutine, Iterable, Set, Union
from pandas import DataFrame
from abc import ABC, abstractclassmethod, abstractproperty
import asyncio

class IGroup(IElement):
    @abstractproperty
    def elements(self)->List[IElement]:# type: ignore 
        pass

class Sequence(IGroup, UserList):
    def __init__(self, name: str, pipeline: 'Pipeline', step: int, elements:Set[IElement], level: Optional[int] = 0, parent:Optional[IElement]=None) -> None:
        IElement.__init__(self, pipeline=pipeline, step=step, level=level, parent=parent, name=name)
        UserList.__init__(self, elements)

    def __iter__(self) -> Iterator['IElement']:
        return super().__iter__()

    async def run(self, source:DataFrame)->DataFrame:
        result:DataFrame=source
        async def subrun(t:IElement)->DataFrame: #type: ignore
                try:
                    await t.run(source=result)
                except Exception as e:
                    ... #TODO: code it
        if len(self.data)>0:
            [await subrun(t) for t in self.data]
        return result

class IParalellGenerator(ABC):
    @abstractclassmethod
    def __next__(self):
        pass
    @abstractclassmethod
    def __iter__(self):
        pass

class Paralell(IGroup):
    def __init__(self, pipeline: 'Pipeline', step: int, generator:IParalellGenerator, level: Optional[int] = 1, name:Optional[str]=None, parent:Optional[IElement]=None) -> None:
        super().__init__(pipeline=pipeline, step=step, level=level, parent=parent, name=name)
        self.generator=generator

    @abstractclassmethod
    async def _post_processing(self, source:DataFrame)->DataFrame:
        raise NotImplementedError
    
    async def run(self, source:DataFrame)->DataFrame:
        await asyncio.gather(*(c.run(source) for c in iter(self.generator)))
        return await self._post_processing(source)
    
class Fork(IGroup):
    def __init__(self, pipeline: 'Pipeline', step: int, branch:IGroup, level: Optional[int] = 0, parent: Optional['IElement'] = None, name: Optional[str]=None) -> None:
        super().__init__(pipeline=pipeline, step=step, level=level, parent=parent, name=name)
        self.branch=branch
    
    async def run(self, source:DataFrame)->DataFrame:
        await self.branch.run(source=source.copy())
        return source

class SubPipeline(IGroup):
    def __init__(self, pipeline: 'Pipeline', sub_pipeline:Union['Pipeline', str], step: int, level: Optional[int] = 0, parent: Optional['IElement'] = None, name: Optional[str]=None) -> None:
        super().__init__(pipeline=pipeline, step=step, level=level, parent=parent, name=name)
        self._subpipe=sub_pipeline if isinstance(sub_pipeline, Pipeline) else Pipeline.pipeline(sub_pipeline)
    
    async def run(self, source:DataFrame)->DataFrame:
        return await self._subpipe.run(source=source)
    
    @property
    def elements(self) -> List[IElement]:
        return self._subpipe.elements