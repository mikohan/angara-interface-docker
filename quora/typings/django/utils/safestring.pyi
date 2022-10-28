"""
This type stub file was generated by pyright.
"""

from typing import Any, overload

_SD = ...
class SafeData:
    def __html__(self: _SD) -> _SD:
        ...
    


class SafeText(str, SafeData):
    @overload
    def __add__(self, rhs: SafeText) -> SafeText:
        ...
    
    @overload
    def __add__(self, rhs: str) -> str:
        ...
    
    @overload
    def __iadd__(self, rhs: SafeText) -> SafeText:
        ...
    
    @overload
    def __iadd__(self, rhs: str) -> str:
        ...
    


SafeString = SafeText
_C = ...
@overload
def mark_safe(s: _SD) -> _SD:
    ...

@overload
def mark_safe(s: _C) -> _C:
    ...

@overload
def mark_safe(s: Any) -> SafeText:
    ...

