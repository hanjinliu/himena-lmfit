from himena.plugins import register_widget_class
from himena_lmfit.consts import Types


def _register():
    from .model import QLmfitModelWidget
    from .model_result import QLmfitModelResultWidget
    from .parameters import QLmfitParametersWidget

    register_widget_class(Types.MODEL, QLmfitModelWidget)
    register_widget_class(Types.MODEL_RESULT, QLmfitModelResultWidget)
    register_widget_class(Types.PARAMS, QLmfitParametersWidget)


_register()
del _register
