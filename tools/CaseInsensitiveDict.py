# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import datetime
from typing import (
    Any,
    Dict,
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    Optional,
    Tuple,
    Union,
)
from datetime import timezone

TZ_UTC = timezone.utc  # type: ignore


class CaseInsensitiveDict(MutableMapping[str, Any]):
    """
    NOTE: This implementation is heavily inspired from the case insensitive dictionary from the requests library.
    Thank you !!
    Case insensitive dictionary implementation.
    The keys are expected to be strings and will be stored in lower case.
    case_insensitive_dict = CaseInsensitiveDict()
    case_insensitive_dict['Key'] = 'some_value'
    case_insensitive_dict['key'] == 'some_value' #True
    """

    def __init__(
        self,
        data: Optional[Union[Mapping[str, Any], Iterable[Tuple[str, Any]]]] = None,
        **kwargs: Any
    ) -> None:
        self._store: Dict[str, Any] = {}
        if data is None:
            data = {}

        self.update(data, **kwargs)

    def copy(self) -> "CaseInsensitiveDict":
        return CaseInsensitiveDict(self._store.values())

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set the `key` to `value`. The original key will be stored with the value
        """
        self._store[key.lower()] = (key, value)

    def __getitem__(self, key: str) -> Any:
        return self._store[key.lower()][1]

    def __delitem__(self, key: str) -> None:
        del self._store[key.lower()]

    def __iter__(self) -> Iterator[str]:
        return (key for key, _ in self._store.values())

    def __len__(self) -> int:
        return len(self._store)

    def lowerkey_items(self):
        return (
            (lower_case_key, pair[1]) for lower_case_key, pair in self._store.items()
        )

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Mapping):
            other = CaseInsensitiveDict(other)
        else:
            return False

        return dict(self.lowerkey_items()) == dict(other.lowerkey_items())

    def __repr__(self) -> str:
        return str(dict(self.items()))
