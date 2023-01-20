from src.pipeline import IElement, Pipeline
from typing import Optional, List, Iterator
from collections import UserList
from src.pipeline.transformers.transformation import ITransformation
from pandas import DataFrame
from src.pipeline.groups import Sequence

class Transformer(Sequence):
    def __init__(self, name: str, pipeline: 'Pipeline', step: int, transformations:List['ITransformation'], level: Optional[int] = 1) -> None:
        Sequence(name, pipeline, step, transformations, level)
    