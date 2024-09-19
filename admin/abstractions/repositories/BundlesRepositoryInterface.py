from abc import ABC, abstractmethod

from abstractions.repositories import CRUDRepositoryInterface
from domain.dto.bundle import BundleCreateDTO, BundleUpdateDTO
from domain.models import Bundle


class BundlesRepositoryInterface(
    CRUDRepositoryInterface[
        Bundle, BundleCreateDTO, BundleUpdateDTO
    ],
    ABC,
):
    @abstractmethod
    async def add_worker_to_bundle(self, worker_id: str, bundle_id: str) -> None:
        ...
