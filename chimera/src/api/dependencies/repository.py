import typing
from src.repository.rag.base import BaseRAGRepository


def get_rag_repository(
    repo_type: typing.Type[BaseRAGRepository],
) -> typing.Callable[[], BaseRAGRepository]:
    def _get_repo() -> BaseRAGRepository:
        return repo_type()

    return _get_repo
