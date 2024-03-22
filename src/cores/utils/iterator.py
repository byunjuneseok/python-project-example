from typing import Any, Generator, List


def chunk_array(array: List[Any], size: int) -> Generator[List[Any], None, None]:
    yield from (array[i : i + size] for i in range(0, len(array), size))
