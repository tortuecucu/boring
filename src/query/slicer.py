from abc import ABC, abstractclassmethod
from numbers import Number
from collections import namedtuple
from collections.abc import Generator
from datetime import datetime

Slice=namedtuple('Slice', ('start', 'end'))

class IntSlicer(Generator):
    def __init__(self, start:int, stop:int, step:int=1) -> None:
        assert step > 0
        self.start=start
        self.i=start
        self.stop=stop
        self.step=step
    
    def send(self, value):
        if self.i < self.stop and (self.i + self.step - 1) <= self.stop:
            out = self.i
            self.i = self.i + self.step
            return Slice(out, self.i-1)
        elif self.step > -1:
            slice = Slice(self.i, self.stop)
            self.i=self.stop
            self.step=-1
            return slice
        raise StopIteration
    
    def throw(self, typ, val=None, tb=None):
        super().throw(typ, val, tb)
    
class DateSlicer(IntSlicer):
    def __init__(self, start: datetime, stop: datetime, step: int = 1) -> None:
        #TODO: supprimer step et remplacer par la bonne variable
        super().__init__(start, stop, step)

    def send(self, value):
        raise NotImplementedError #TODO: code it
