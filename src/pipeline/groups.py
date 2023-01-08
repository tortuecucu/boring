from src.pipeline import IElement, Pipeline
from collections import UserList
from typing import Optional, List, Iterator, Coroutine, Iterable
from pandas import DataFrame
from abc import ABC, abstractclassmethod
import asyncio

class Sequence(IElement, UserList):
    def __init__(self, name: str, pipeline: 'Pipeline', step: int, elements:List[IElement], level: Optional[int] = 1) -> None:
        IElement().__init__(name, pipeline, step, level)
        UserList().__init__(elements)

    def __iter__(self) -> Iterator['IElement']:
        return super().__iter__()

    async def run(self, source:DataFrame)->DataFrame:
        result:DataFrame=source
        async def subrun(t:IElement)->DataFrame:
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

class Paralell(IElement):
    def __init__(self, name: str, pipeline: 'Pipeline', step: int, generator:IParalellGenerator, level: Optional[int] = 1) -> None:
        super().__init__(name, pipeline, step, level)
        self.generator=generator

    @abstractclassmethod
    async def _post_processing(self, source:DataFrame)->DataFrame:
        raise NotImplementedError
    
    async def run(self, source:DataFrame)->DataFrame:
        await asyncio.gather(*(c.run(source) for c in iter(self.generator)))
        return await self._post_processing(source)