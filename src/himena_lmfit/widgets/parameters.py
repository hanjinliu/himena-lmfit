from __future__ import annotations
from typing import TYPE_CHECKING
from himena import WidgetDataModel
from qtpy import QtCore, QtGui

from himena.plugins import validate_protocol
from himena.consts import MonospaceFontFamily
from himena_builtins.qt.widgets._table_components import QTableBase

from himena_lmfit._lazy_import import lmfit
from himena_lmfit.consts import Types


class QParametersTableModel(QtCore.QAbstractTableModel):
    def __init__(self, params: lmfit.Parameters, parent=None):
        super().__init__(parent)
        self._params = params
        self._names: list[str] = [param for param in params]
        self._header = ["Value", "Bound", "Expr"]
        self._flags = QtCore.Qt.ItemFlag.ItemIsSelectable

    def rowCount(self, parent=None):
        return len(self._params)

    def columnCount(self, parent=None):
        return len(self._header)

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        col = index.column()
        if role in (
            QtCore.Qt.ItemDataRole.DisplayRole,
            QtCore.Qt.ItemDataRole.ToolTipRole,
        ):
            param = self._params[self._names[index.row()]]
            if not isinstance(param, lmfit.Parameter):
                return None
            if col == 0:
                if not param._vary and param.expr is None:
                    sval = f"{param.value:.6g} (fixed)"
                elif param.stderr is not None:
                    sval = f"{param.value:.6g} +/- {param.stderr:.3g}"
                else:
                    sval = f"{param.value:.6g}"
                return sval
            elif col == 1:
                return f"[{param.min!r}:{param.max!r}]"
            elif col == 2:
                if param.expr is None:
                    return ""
                return param.expr
            else:
                return None

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if orientation == QtCore.Qt.Orientation.Horizontal:
                return self._header[section]
            else:
                param = self._params[self._names[section]]
                if not isinstance(param, lmfit.Parameter):
                    return None
                return param.name
        if role == QtCore.Qt.ItemDataRole.TextAlignmentRole:
            if orientation == QtCore.Qt.Orientation.Vertical:
                return (
                    QtCore.Qt.AlignmentFlag.AlignRight
                    | QtCore.Qt.AlignmentFlag.AlignVCenter
                )
            else:
                return QtCore.Qt.AlignmentFlag.AlignCenter
        if role == QtCore.Qt.ItemDataRole.FontRole:
            if orientation == QtCore.Qt.Orientation.Vertical:
                return QtGui.QFont(MonospaceFontFamily)


class QLmfitParametersWidget(QTableBase):
    __himena_widget_id__ = "himena-lmfit:QLmfitParametersWidget"
    __himena_display_name__ = "lmfit Parameters"

    def __init__(self):
        super().__init__()
        self.setFont(QtGui.QFont(MonospaceFontFamily))
        self.setModel(QParametersTableModel(lmfit.Parameters()))

    @validate_protocol
    def update_model(self, model: WidgetDataModel):
        fmodel = model.value
        if not isinstance(fmodel, lmfit.Parameters):
            raise TypeError("model must be a lmfit.Parameters")
        self.setModel(QParametersTableModel(fmodel))
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)
        self.update()

    @validate_protocol
    def to_model(self) -> WidgetDataModel:
        return WidgetDataModel(
            value=self.model()._params,
            type=self.model_type(),
            title="Parameters",
        )

    @validate_protocol
    def model_type(self) -> str:
        return Types.PARAMS

    if TYPE_CHECKING:

        def model(self) -> QParametersTableModel: ...
