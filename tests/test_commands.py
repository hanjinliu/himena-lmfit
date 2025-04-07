import numpy as np
import lmfit
from pytestqt.qtbot import QtBot
from himena.widgets import MainWindow

def test_guess_params(himena_ui: MainWindow, qtbot: QtBot):
    x = np.arange(10)
    win = himena_ui.add_object({"x": x, "y": x**2 /4 - x + 2}, type="dataframe")
    himena_ui.exec_action(
        "himena_lmfit:models:build-quadratic-model", with_params={"prefix": "test_"}
    )
    win_model = himena_ui.current_window
    out0 = himena_ui.exec_action(
        "himena_lmfit:models:guess-params",
        with_params={"table": win, "x": ((0, 10), (0, 1)), "y": ((0, 10), (1, 2))},
        window_context=win_model,
    )
    out1 = himena_ui.exec_action(
        "himena_lmfit:models:guess-params-from-table",
        with_params={"function": win_model.to_model()},
        window_context=win,
    )
    assert isinstance(p0 := out0.value, lmfit.Parameters)
    assert isinstance(p1 := out1.value, lmfit.Parameters)
    assert {k: v.value for k, v in p0.items()} == {k: v.value for k, v in p1.items()}
