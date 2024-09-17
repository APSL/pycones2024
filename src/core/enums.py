from enum import Enum


class Permissions(str, Enum):
    POSTAL_CLERK = "Postal clerk"
    COURIER = "Courier"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    def __str__(self) -> str:
        return self.value


class VersionAPI(str, Enum):
    LATEST = "latest"
    V1 = "v1"
    V2 = "v2"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    def __str__(self) -> str:
        return self.value
