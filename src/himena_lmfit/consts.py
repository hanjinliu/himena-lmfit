from himena.plugins import configure_submenu


class Menus:
    LMFIT = ["tools/lmfit", "/model_menu/lmfit"]
    LMFIT_MODELS = ["tools/lmfit/models"]
    LMFIT_OPTIMIZE = ["tools/lmfit/optimize"]
    LMFIT_RESULTS = ["tools/lmfit/results"]


configure_submenu(Menus.LMFIT, title="LMfit")


class Types:
    MODEL = "lmfit-model"
    PARAMS = "dict.lmfit-model-params"
    MODEL_RESULT = "lmfit-model-result"
