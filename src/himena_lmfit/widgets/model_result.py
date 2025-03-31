from __future__ import annotations

from qtpy import QtWidgets as QtW

from himena import WidgetDataModel
from himena.plugins import validate_protocol
from himena_lmfit._lazy_import import lmfit
from himena_lmfit.consts import Types


class QLmfitModelResultWidget(QtW.QWidget):
    def __init__(self):
        self._lmfit_model_result: lmfit.model.ModelResult | None = None
        super().__init__()
        self._text = QtW.QPlainTextEdit(self)
        self._text.setReadOnly(True)
        layout = QtW.QVBoxLayout(self)
        layout.addWidget(self._text)

    @validate_protocol
    def update_model(self, model: WidgetDataModel):
        fmodel = model.value
        if not isinstance(fmodel, lmfit.model.ModelResult):
            raise TypeError("model must be a lmfit.model.ModelResult")
        self._lmfit_model_result = fmodel
        description = "\n".join(
            [
                f"Name: {self._lmfit_model_result.model.name}",
                f"Parameters: {self._lmfit_model_result.params}",
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
