from himena import Parametric, StandardType, WidgetDataModel
from himena.plugins import register_function, configure_gui
from himena_builtins.tools.text import compile_as_function

from himena_lmfit._lazy_import import lmfit
from himena_lmfit._magicgui import ParamEdit
from himena_lmfit.consts import Menus, Types


@register_function(
    menus=Menus.LMFIT_MODELS,
    title="Build lmfit model",
    types=[StandardType.TEXT],
    command_id="himena_lmfit:build-lmfit-model",
)
def build_lmfit_model(model: WidgetDataModel) -> WidgetDataModel:
    fmodel = compile_as_function(model)
    return WidgetDataModel(
        value=lmfit.Model(fmodel.value),
        type=Types.MODEL,
        title=fmodel.title,
    )


@register_function(
    menus=Menus.LMFIT_MODELS,
    title="Constant",
    command_id="himena_lmfit:models:build-constant-model",
)
def build_constant_model() -> Parametric:
    """Build a constant model"""

    @configure_gui(c={"widget_type": ParamEdit})
    def create(
        prefix: str = "",
        name: str = "",
        c=None,
    ) -> WidgetDataModel:
        """Create a constant model"""
        return _create_model(lmfit.models.ConstantModel(prefix=prefix))

    return create


@register_function(
    menus=Menus.LMFIT_MODELS,
    title="Linear",
    command_id="himena_lmfit:models:build-linear-model",
)
def build_linear_model() -> Parametric:
    """Build a linear model"""

    @configure_gui(
        slope={"widget_type": ParamEdit}, intercept={"widget_type": ParamEdit}
    )
    def create(
        prefix: str = "",
        name: str = "",
        slope=None,
        intercept=None,
    ) -> WidgetDataModel:
        """Create a linear model"""
        fmodel = lmfit.models.LinearModel(prefix=prefix, name=name)
        if slope:
            fmodel.set_param_hint("slope", **slope)
        if intercept:
            fmodel.set_param_hint("intercept", **intercept)
        return _create_model(lmfit.models.LinearModel(prefix=prefix, name=name))

    return create


@register_function(
    menus=Menus.LMFIT_MODELS,
    title="Quadratic",
    command_id="himena_lmfit:models:build-quadratic-model",
)
def build_quadratic_model() -> Parametric:
    """Build a quadratic model"""

    @configure_gui
    def create(prefix: str = "") -> WidgetDataModel:
        """Create a quadratic model"""
        return _create_model(lmfit.models.QuadraticModel(prefix=prefix))

    return create


@register_function(
    menus=Menus.LMFIT_MODELS,
    title="Polynomial",
    command_id="himena_lmfit:models:build-polynomial-model",
)
def build_polynomial_model() -> Parametric:
    """Build a polynomial model"""

    @configure_gui(degree={"widget_type": ParamEdit})
    def create(prefix: str = "", degree: int = 2) -> WidgetDataModel:
        """Create a polynomial model"""
        fmodel = lmfit.models.PolynomialModel(degree=degree, prefix=prefix)
        return _create_model(fmodel)

    return create


@register_function(
    menus=Menus.LMFIT_MODELS,
    title="Exponential",
    command_id="himena_lmfit:models:build-exponential-model",
)
def build_exponential_model() -> Parametric:
    """Build an exponential decay model"""

    @configure_gui
    def create(prefix: str = "") -> WidgetDataModel:
        """Create an exponential decay model"""
        return _create_model(lmfit.models.ExponentialModel(prefix=prefix))

    return create


@register_function(
    menus=Menus.LMFIT_MODELS,
    title="Gaussian",
    command_id="himena_lmfit:models:build-gaussian-model",
)
def build_gaussian_model() -> Parametric:
    """Build a Gaussian model"""

    @configure_gui
    def create(prefix: str = "") -> WidgetDataModel:
        """Create a Gaussian model"""
        return _create_model(lmfit.models.GaussianModel(prefix=prefix))

    return create


@register_function(
    menus=Menus.LMFIT_MODELS,
    title="Lorentzian",
    command_id="himena_lmfit:models:build-lorentzian-model",
)
def build_lorentzian_model() -> Parametric:
    """Build a Lorentzian model"""

    @configure_gui
    def create(prefix: str = "") -> WidgetDataModel:
        """Create a Lorentzian model"""
        return _create_model(lmfit.models.LorentzianModel(prefix=prefix))

    return create


@register_function(
    menus=Menus.LMFIT_MODELS,
    title="Sine",
    command_id="himena_lmfit:models:build-sine-model",
)
def build_sine_model() -> Parametric:
    """Build a sine model"""

    @configure_gui
    def create(prefix: str = "") -> WidgetDataModel:
        """Create a sine model"""
        return _create_model(lmfit.models.SineModel(prefix=prefix))

    return create


def _create_model(fmodel: "lmfit.Model") -> WidgetDataModel:
    """Create a model"""
    return WidgetDataModel(
        value=fmodel,
        type=Types.MODEL,
        title=fmodel.name,
    )
