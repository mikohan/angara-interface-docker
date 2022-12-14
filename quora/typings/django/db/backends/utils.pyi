"""
This type stub file was generated by pyright.
"""

import types
from datetime import date, datetime, time
from decimal import Decimal
from typing import Any, ContextManager, Dict, Iterator, List, Mapping, Optional, Sequence, Tuple, Type, Union
from uuid import UUID

logger: Any
_SQLType = Union[None, bool, int, float, Decimal, str, bytes, date, datetime, UUID, Tuple[Any, ...], List[Any]]
_ExecuteParameters = Optional[Union[Sequence[_SQLType], Mapping[str, _SQLType]]]
class CursorWrapper:
    cursor: Any = ...
    db: Any = ...
    def __init__(self, cursor: Any, db: Any) -> None:
        ...
    
    WRAP_ERROR_ATTRS: Any = ...
    def __getattr__(self, attr: str) -> Any:
        ...
    
    def __iter__(self) -> Iterator[Tuple[Any, ...]]:
        ...
    
    def __enter__(self) -> CursorWrapper:
        ...
    
    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException], tb: Optional[types.TracebackType]) -> None:
        ...
    
    def callproc(self, procname: str, params: List[Any] = ..., kparams: Dict[str, int] = ...) -> Any:
        ...
    
    def execute(self, sql: str, params: _ExecuteParameters = ...) -> Any:
        ...
    
    def executemany(self, sql: str, param_list: Sequence[_ExecuteParameters]) -> Any:
        ...
    


class CursorDebugWrapper(CursorWrapper):
    cursor: Any
    db: Any
    def debug_sql(self, sql: Optional[str] = ..., params: Optional[Union[_ExecuteParameters, Sequence[_ExecuteParameters]]] = ..., use_last_executed_query: bool = ..., many: bool = ...) -> ContextManager[None]:
        ...
    


def typecast_date(s: Optional[str]) -> Optional[date]:
    ...

def typecast_time(s: Optional[str]) -> Optional[time]:
    ...

def typecast_timestamp(s: Optional[str]) -> Optional[date]:
    ...

def rev_typecast_decimal(d: Decimal) -> str:
    ...

def split_identifier(identifier: str) -> Tuple[str, str]:
    ...

def truncate_name(identifier: str, length: Optional[int] = ..., hash_len: int = ...) -> str:
    ...

def format_number(value: Optional[Decimal], max_digits: Optional[int], decimal_places: Optional[int]) -> Optional[str]:
    ...

def strip_quotes(table_name: str) -> str:
    ...

