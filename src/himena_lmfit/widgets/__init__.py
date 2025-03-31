from himena.plugins import register_widget_class
from himena_lmfit.consts import Types


def _register():
    from .models import QLmfitModelWidget
    from .model_result import QLmfitModelResultWidget

    register_widget_class(Types.MODEL, QLmfitModelWidget)
    register_widget_class(Types.MODEL_RESULT, QLmfitModelResultWidget)


_register()
del _register
