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


MINIMZE_METHODS = [
    "leastsq",
    "least_squares",
    "differential_evolution",
    "brute",
    "basinhopping",
    "ampgo",
    "nelder",
    "lbfgsb",
    "powell",
    "cg",
    "newton",
    "cobyla",
    "bfgs",
    "tnc",
    "trust",
    "trust",
    "trust",
    "trust",
    "dogleg",
    "slsqp",
    "emcee",
    "shgo",
    "dual_annealing",
]
