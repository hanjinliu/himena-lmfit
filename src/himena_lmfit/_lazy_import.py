from typing import TYPE_CHECKING


class LazyLmfit:
    def __getattr__(self, key: str):
        import lmfit

        return getattr(lmfit, key)


if TYPE_CHECKING:
    import lmfit
else:
    lmfit = LazyLmfit()

__all__ = ["lmfit"]
