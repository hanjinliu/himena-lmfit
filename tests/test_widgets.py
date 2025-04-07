import numpy as np
from pytestqt.qtbot import QtBot
import lmfit
from himena.testing import WidgetTester
from himena_lmfit.widgets.model import QLmfitModelWidget
from himena_lmfit.widgets.model_result import QLmfitModelResultWidget
from himena_lmfit.widgets.parameters import QLmfitParametersWidget

def test_lmfit_model_widget(qtbot: QtBot):
    widget = QLmfitModelWidget()
    qtbot.addWidget(widget)
    with WidgetTester(widget) as tester:
        tester.update_model(value=lmfit.models.StepModel())
        tester.to_model()

def test_lmfit_model_result_widget(qtbot: QtBot):
    widget = QLmfitModelResultWidget()
    qtbot.addWidget(widget)
    m = lmfit.models.StepModel()
    result = m.fit(np.array([0.1, 0, 0.1, 1.2, 1.1]), x=np.arange(5))
    with WidgetTester(widget) as tester:
        tester.update_model(value=result)
        tester.to_model()

def test_lmfit_parameters_widget(qtbot: QtBot):
    widget = QLmfitParametersWidget()
    qtbot.addWidget(widget)
    m = lmfit.models.StepModel()
    params = m.guess(np.array([0.1, 0, 0.1, 1.2, 1.1]), x=np.arange(5))
    with WidgetTester(widget) as tester:
        tester.update_model(value=params)
        tester.to_model()
