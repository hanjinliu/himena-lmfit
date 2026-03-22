from himena import Parametric, StandardType, WidgetDataModel
from himena.plugins import register_function, configure_gui
from himena_builtins.tools.text import compile_as_function

from himena_lmfit._lazy_import import lmfit
from himena_lmfit._magicgui import ParamEdit
from himena_lmfit.consts import Menus, Types


@register_function(
    menus=Menus.LMFIT_MODELS,
    title="Build lmfit model",
    types=[StandardType.TEXT, StandardType.FUNCTION],
    command_id="himena_lmfit:models-00_user:build-lmfit-model",
)
def build_lmfit_model(model: WidgetDataModel) -> WidgetDataModel:
    """Built a lmfit model from a text or function"""
    if model.is_subtype_of(StandardType.TEXT):
        fmodel = compile_as_function(model)
    elif model.is_subtype_of(StandardType.FUNCTION):
        fmodel = model
    else:
        raise TypeError("model must be a text or function")
    return WidgetDataModel(
        value=lmfit.Model(fmodel.value),
        type=Types.MODEL,
        title=fmodel.title,
    )


@register_function(
    menus=Menus.LMFIT_MODELS,
    title="Expression",
    command_id="himena_lmfit:models-00_user:build-expression-model",
)
def build_expression_model() -> Parametric:
    """Build an expression model"""

    def create(prefix: str = "", expr: str = "amp * sin(x*phase)") -> WidgetDataModel:
        """Create an expression model"""
        fmodel = lmfit.models.ExpressionModel(expr, prefix=prefix)
        return _create_model(fmodel)

    return create


@register_function(
    menus=Menus.LMFIT_MODELS,
    title="Constant",
    command_id="himena_lmfit:models-00_simple:build-constant-model",
)
def build_constant_model() -> Parametric:
    """Build a constant model"""

    @configure_gui(c={"widget_type": ParamEdit})
    def create(
        prefix: str = "",
        c=None,
    ) -> WidgetDataModel:
        """Create a constant model"""
        return _create_model(lmfit.models.ConstantModel(prefix=prefix, c=c))

    return create


@register_function(
    menus=Menus.LMFIT_MODELS,
    title="Linear",
    command_id="himena_lmfit:models-00_simple:build-linear-model",
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
    command_id="himena_lmfit:models-00_simple:build-quadratic-model",
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
    command_id="himena_lmfit:models-00_simple:build-polynomial-model",
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
    command_id="himena_lmfit:models-01_continuous:build-exponential-model",
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
    command_id="himena_lmfit:models-01_continuous:build-gaussian-model",
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
    command_id="himena_lmfit:models-01_continuous:build-lorentzian-model",
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
    command_id="himena_lmfit:models-01_continuous:build-sine-model",
)
def build_sine_model() -> Parametric:
    """Build a sine model"""

    @configure_gui
    def create(prefix: str = "") -> WidgetDataModel:
        """Create a sine model"""
        return _create_model(lmfit.models.SineModel(prefix=prefix))

    return create


@register_function(
    menus=Menus.LMFIT_MODELS,
    title="Step",
    command_id="himena_lmfit:models-02_discrete:build-step-model",
)
def build_step_model() -> Parametric:
    """Build a step model"""

    @configure_gui
    def create(prefix: str = "") -> WidgetDataModel:
        """Create a step model"""
        return _create_model(lmfit.models.StepModel(prefix=prefix))

    return create


@register_function(
    menus=Menus.LMFIT_MODELS,
    title="Rectangle",
    command_id="himena_lmfit:models-02_discrete:build-rectangle-model",
)
def build_rectangle_model() -> Parametric:
    """Build a rectangle model"""

    @configure_gui
    def create(prefix: str = "") -> WidgetDataModel:
        """Create a rectangle model"""
        return _create_model(lmfit.models.RectangleModel(prefix=prefix))

    return create


@register_function(
    menus=Menus.LMFIT_MODELS,
    types=[Types.MODEL],
    title="Linear transform of model",
    command_id="himena_lmfit:models:linear-transform-model",
)
def linear_transform_model(model: WidgetDataModel) -> Parametric:
    def run(amp: float = 1.0, offset: float = 0.0) -> WidgetDataModel:
        """Create a linear transform of a model"""
        if not isinstance(fmod := model.value, lmfit.Model):
            raise TypeError("model must be a lmfit.Model")

        def func_new(*args, **kwargs):
            """Transform the function"""
            return amp * fmod.func(*args, **kwargs) + offset

        fmod_new = lmfit.Model(func_new, prefix=fmod.prefix)
        return _create_model(fmod_new)

    return run


def _create_model(fmodel: "lmfit.Model") -> WidgetDataModel:
    """Create a model"""
    return WidgetDataModel(value=fmodel, type=Types.MODEL, title=fmodel.name)
