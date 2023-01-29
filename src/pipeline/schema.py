from typing import Set, Union
from pathlib import Path
from jsonschema import validate, ValidationError
import json

class Schema():
    _instances=[]

    def __init__(self, path:Union[Path,str]) -> None:
        if not isinstance(path, Path): path=Path(path)
        assert path.exists(), "schema file does not exists"
        self._data=self._data(path)
        

    @staticmethod
    def _data(path:Path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                data=json.load(file)
            with open('schemas/jsonschema.json', 'r') as shema_file:
                schema=json.load(shema_file)
            validate(instance=data, schema=schema)
            return data
        except ValidationError as e:
            raise e

    @property
    def requirements(self)->Set[str]:
        ...
    
    @property
    def name(self)->str:
        ...
    
    @classmethod
    def schema(cls, name:str)->'Schema':
        try:
            path=Path(f"schemas/{name}.json")
            return Schema(path)
        except Exception as e:
            raise ValueError from e