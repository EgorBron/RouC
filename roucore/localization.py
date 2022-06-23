from disnake.i18n import LocalizationProtocol
import os, ujson
from collections import defaultdict
from pathlib import Path
from typing import (
    DefaultDict,
    Dict,
    Optional,
    Set,
    Union,
)

class LocalizationKeyError(Exception): pass

class Localizator(LocalizationProtocol):
    """
    Manages a key-value mapping of localizations using ``.json`` files.

    .. versionadded:: 2.5

    Attributes
    ------------
    strict: :class:`bool`
        Specifies whether :meth:`.get` raises an exception if localizations for a provided key couldn't be found.
    """

    def __init__(self, *, strict: bool=False):
        self.strict = strict

        self._loc = defaultdict(dict)
        self._paths: Set[Path] = set()

    def get(self, key: str) -> Optional[Dict[str, str]]:
        """
        Returns localizations for the specified key.

        Parameters
        ----------
        key: :class:`str`
            The lookup key.

        Raises
        ------
        LocalizationKeyError
            No localizations for the provided key were found.
            Raised only if :attr:`strict` is enabled, returns ``None`` otherwise.

        Returns
        -------
        Optional[Dict[:class:`str`, :class:`str`]]
            The localizations for the provided key.
            Returns ``None`` if no localizations could be found and :attr:`strict` is disabled.
        """
        outdict = {}
        for i in key.split('.'):
            outdict = self._loc.get(i) if outdict == {} else outdict.get(i)
        if outdict == {} and self.strict:
            raise LocalizationKeyError(f'Error: No localizations for key \'{key}\' found')
        return outdict

    def load(self, path: Union[str, os.PathLike]) -> None:
        """
        Adds localizations from the provided path to the store.
        If the path points to a file, the file gets loaded.
        If it's a directory, all ``.json`` files in that directory get loaded (non-recursive).

        Parameters
        ----------
        path: Union[:class:`str`, :class:`os.PathLike`]
            The path to the file/directory to load.

        Raises
        ------
        RuntimeError
            The provided path is invalid or couldn't be loaded
        """

        path = Path(path)

        if path.is_file():
            self._load_file(path)
        elif path.is_dir():
            for file in path.glob("*.json"):
                if not file.is_file():
                    continue
                self._load_file(file)
        else:
            raise RuntimeError(f"Path '{path}' does not exist or is not a directory/file")

        self._paths.add(path)

    def reload(self) -> None:
        """
        Clears localizations and reloads all previously loaded files/directories again.
        If an exception occurs, the previous data gets restored and the exception is re-raised.
        See :func:`~LocalizationStore.load` for possible raised exceptions.
        """

        old = self._loc
        try:
            self._loc = defaultdict(dict)
            for path in self._paths:
                self.load(path)
        except Exception:
            # restore in case of error
            self._loc = old
            raise

    def _load_file(self, path: Path) -> None:
        try:
            if path.suffix != ".json":
                raise ValueError(f"not a .json file")
            locale = path.stem

            self._loc = ujson.loads(path.read_text("utf-8"))
        except Exception as e:
            raise RuntimeError(f"Unable to load '{path}': {e}") from e