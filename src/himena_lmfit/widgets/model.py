from __future__ import annotations

from qtpy import QtWidgets as QtW

from himena import WidgetDataModel
from himena.plugins import validate_protocol
from himena_lmfit._lazy_import import lmfit
from himena_lmfit.consts import Types


class QLmfitModelWidget(QtW.QWidget):
    __himena_widget_id__ = "himena-lmfit:QLmfitModelWidget"
    __himena_display_name__ = "lmfit Model"

    def __init__(self):
        self._lmfit_model = lmfit.models.ConstantModel()
        super().__init__()
        self._text = QtW.QPlainTextEdit(self)
        self._text.setReadOnly(True)
        layout = QtW.QVBoxLayout(self)
        layout.addWidget(self._text)

    @validate_protocol
    def update_model(self, model: WidgetDataModel):
        fmodel = model.value
        if not isinstance(fmodel, lmfit.Model):
            raise TypeError("model must be a lmfit.Model")
        self._lmfit_model = fmodel
        description = "\n".join(
            [
                f"Name: {self._lmfit_model.name}",
                f"Parameters: {self._lmfit_model.param_names}",
            ]
        )
        self._text.setPlainText(description)

    @validate_protocol
    def to_model(self) -> WidgetDataModel:
        return WidgetDataModel(
            value=self._lmfit_model,
            type=Types.MODEL,
            title=self._lmfit_model.name,
        )

    @validate_protocol
    def model_type(self) -> str:
        return Types.MODEL
