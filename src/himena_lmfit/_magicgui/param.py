from __future__ import annotations

import numpy as np
from magicgui.types import Undefined
from magicgui.widgets.bases import ValuedContainerWidget
from himena.qt.magicgui import FloatEdit, get_type_map
from himena_lmfit._lazy_import import lmfit


class ParamEdit(ValuedContainerWidget[lmfit.Parameter]):
    """A widget for editing lmfit parameters."""

    def __init__(self, value, **kwargs):
        self._value = FloatEdit()
        self._min = FloatEdit()
        self._max = FloatEdit()
        super().__init__(
            value=value,
            widgets=[self._value, self._min, self._max],
            layout="horizontal",
            **kwargs,
        )
        self._value.changed.connect(self._on_widget_state_changed)
        self._min.changed.connect(self._on_widget_state_changed)
        self._max.changed.connect(self._on_widget_state_changed)

    def get_value(self) -> lmfit.Parameter | None:
        _min, _max = self._min.value, self._max.value
        if self._value is None and _min is None and _max is None:
            return None
        if _min is None:
            _min = -np.inf
        if _max is None:
            _max = np.inf
        return lmfit.Parameter(self.name, self._value.value, min=_min, max=_max)

    def set_value(self, value) -> None:
        if value is None or value is Undefined:
            param = lmfit.Parameter(self.name)
        elif isinstance(value, dict):
            param = lmfit.create_params(name=self.name, **value)
        elif isinstance(value, lmfit.Parameter):
            param = value
        else:
            raise TypeError("value must be a lmfit.Parameter or a dictionary")

        self._value.value = param.value
        if np.isneginf(_min := param.min):
            self._min.value = None
        else:
            self._min.value = _min
        if np.isposinf(_max := param.max):
            self._max.value = None
        else:
            self._max.value = _max

    def _on_widget_state_changed(self):
        """Update the value when the widget state changes."""
        self.changed.emit(self.get_value())


typemap = get_type_map()
typemap.register_type(lmfit.Parameter, widget_type=ParamEdit)
