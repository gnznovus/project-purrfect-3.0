from abc import ABC, abstractmethod

from .context import RequestContext
from .result import CoreResult


class Handler(ABC):

    @abstractmethod
    async def handle(
        self,
        context: RequestContext
    ) -> CoreResult:
        pass