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
    V1 = "v1"
    V2 = "v2"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    def __str__(self) -> str:
        return self.value

    def __lt__(self, other):
        version = self.value[1:]
        other_version = other.value[1:]
        return float(version) < float(other_version)

    def __eq__(self, other):
        version = self.value[1:]
        other_version = other.value[1:]
        return float(version) == float(other_version)

    def __gt__(self, other):
        version = self.value[1:]
        other_version = other.value[1:]
        return float(version) > float(other_version)
