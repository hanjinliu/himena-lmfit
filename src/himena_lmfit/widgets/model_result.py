from __future__ import annotations

from qtpy import QtWidgets as QtW, QtCore, QtGui

from himena import WidgetDataModel
from himena.consts import MonospaceFontFamily
from himena.plugins import validate_protocol

from himena_lmfit._lazy_import import lmfit
from himena_lmfit.consts import Types
from himena_lmfit.widgets.parameters import QLmfitParametersWidget


class QLmfitModelResultWidget(QtW.QWidget):
    __himena_widget_id__ = "himena-lmfit:QLmfitModelResultWidget"
    __himena_display_name__ = "lmfit Model Result"

    def __init__(self):
        self._lmfit_model_result: lmfit.model.ModelResult | None = None
        super().__init__()
        layout = QtW.QVBoxLayout(self)
        self._name = QtW.QLabel(self)
        self._name.setFont(QtGui.QFont(MonospaceFontFamily))
        self._name.setTextInteractionFlags(
            QtCore.Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self._params = QLmfitParametersWidget()
        self._text = QtW.QPlainTextEdit(self)
        self._text.setReadOnly(True)

        layout.addWidget(self._name)
        layout.addWidget(self._params, 2)
        layout.addWidget(self._text, 1)

    @validate_protocol
    def update_model(self, model: WidgetDataModel):
        fmodel = model.value
        if not isinstance(fmodel, lmfit.model.ModelResult):
            raise TypeError("model must be a lmfit.model.ModelResult")
        self._lmfit_model_result = fmodel
        self._name.setText(str(self._lmfit_model_result.model.name))
        self._params.update_model(
            WidgetDataModel(
                value=self._lmfit_model_result.params,
                type=Types.PARAMS,
            )
        )
        description = "\n".join(
            [
                f"Success: {self._lmfit_model_result.success}",
                f"Message: {self._lmfit_model_result.message}",
            ]
        )
        self._text.setPlainText(description)

    @validate_protocol
    def to_model(self) -> WidgetDataModel:
        return WidgetDataModel(
            value=self._lmfit_model_result,
            type=self.model_type(),
            title=self._lmfit_model_result.model.name,
        )

    @validate_protocol
    def model_type(self) -> str:
        return Types.MODEL_RESULT

    @validate_protocol
    def size_hint(self):
        return (320, 360)
