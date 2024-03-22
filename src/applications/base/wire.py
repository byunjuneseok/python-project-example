from dependency_injector.wiring import Provide
from fastapi import Depends


def Wire(dependency_name: str):
    return Depends(Provide[dependency_name])
