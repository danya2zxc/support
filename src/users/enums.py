from enum import StrEnum, auto
from functools import lru_cache


class Role(StrEnum):
    SENIOR = auto()
    JUNIOR = auto()
    ADMIN = auto()

    @classmethod
    @lru_cache(maxsize=1)
    def users(cls):
        return [cls.SENIOR, cls.JUNIOR]

    @classmethod
    @lru_cache(maxsize=1)
    def users_values(cls):
        return [cls.SENIOR.value, cls.JUNIOR.value]

    @classmethod
    def users_staff(cls):
        return [cls.SENIOR, cls.ADMIN]

    @classmethod
    def staff_values(cls):
        return [cls.SENIOR.value, cls.ADMIN.value]

    @classmethod
    @lru_cache(maxsize=1)
    def choices(cls):
        results = []
        for element in cls:
            _element = (
                element.value,
                element.name.lower().capitalize(),
            )
            results.append(_element)
        return results
