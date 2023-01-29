from pathlib import Path
from typing import Dict

_backups:Dict[Path, Path]={}
#key=source file item=backup file

def backup(path:Path)->None:
    ...
    backup_path:Path=None
    _backups[path]=backup_path

def rollback(path:Path)->None:
    assert path in _backups
    ...
    del _backups[path]