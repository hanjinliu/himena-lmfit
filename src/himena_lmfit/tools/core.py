from himena import Parametric, WidgetDataModel, StandardType, create_model
from himena.widgets import SubWindow
from himena.utils.table_selection import (
    table_selection_gui_option,
    model_to_xy_arrays,
    TABLE_LIKE_TYPES,
)
from himena.plugins import register_function, configure_gui
from himena_lmfit._lazy_import import lmfit
from himena_lmfit._magicgui import ParamEdit
from himena_lmfit.consts import Menus, Types, MINIMZE_METHODS

SelectionType = tuple[tuple[int, int], tuple[int, int]]


def _model_to_xy(model, x, y):
    xout, youts = model_to_xy_arrays(
        model, x, y, allow_empty_x=False, allow_multiple_y=False
    )
    return xout, youts[0]


@register_function(
    menus=Menus.LMFIT_MODELS,
    title="Make parameters",
    types=[Types.MODEL],
    command_id="himena_lmfit:models:make-params",
)
def make_params(model: WidgetDataModel) -> Parametric:
    """Make parameters"""
    # TODO: don't use non-variable parameters
    lmfit_model = _cast_lmfit_model(model)
    kwargs = {name: {"widget_type": ParamEdit} for name in lmfit_model.param_names}

    @configure_gui(gui_options=kwargs)
    def make_param_values(**kwargs) -> WidgetDataModel:
        """Make parameters"""
        params = lmfit_model.make_params(**kwargs)
        return WidgetDataModel(
            value=params,
            type=Types.PARAMS,
            title=f"Parameters of {model.title}",
        )

    return make_param_values


@register_function(
    menus=Menus.LMFIT_OPTIMIZE,
    title="Guess parameters",
    types=[Types.MODEL],
    command_id="himena_lmfit:models:guess-params",
)
def guess_params(model: WidgetDataModel) -> Parametric:
    """Guess parameters"""
    lmfit_model = _cast_lmfit_model(model)

    @configure_gui(
        table={"types": TABLE_LIKE_TYPES},
        x=table_selection_gui_option("table"),
        y=table_selection_gui_option("table"),
    )
    def guess_param_values(
        table: SubWindow,
        x: SelectionType,
        y: SelectionType,
    ) -> WidgetDataModel:
        """Guess parameters"""
        xarr, yarr = _model_to_xy(table.to_model(), x, y)
        params = lmfit_model.guess(yarr.array, xarr.array)
        return WidgetDataModel(
            value=params,
            type=Types.PARAMS,
            title=f"Guessed Parameters of {model.title}",
        )

    return guess_param_values


@register_function(
    menus=Menus.LMFIT_RESULTS,
    title="Convert to DataFrame",
    types=[Types.MODEL_RESULT],
    command_id="himena_lmfit:models:fit-result-to-dataframe",
)
def fit_result_to_dataframe(model: WidgetDataModel) -> WidgetDataModel:
    """Convert lmfit fit results to DataFrame"""

    result = _cast_lmfit_model_result(model)
    independent_var = result.model.independent_vars[0]
    df = {
        independent_var: result.userkws[independent_var],
        "data": result.data,
    }
    df["data_fit"] = result.eval(
        result.params, **{independent_var: df[independent_var]}
    )
    df["uncertainties"] = result.eval_uncertainty()
    if result.weights is not None:
        df["weights"] = result.weights
    return create_model(
        df,
        type=StandardType.DATAFRAME,
        title=f"DataFrame of {model.title}",
    )


@register_function(
    menus=Menus.LMFIT_OPTIMIZE,
    title="Curve fit ...",
    types=[Types.MODEL, StandardType.FUNCTION],
    command_id="himena_lmfit:fit:curve-fit",
)
def curve_fit(model: WidgetDataModel) -> Parametric:
    """Curve fit"""
    lmfit_model = _cast_lmfit_model(model)

    @configure_gui(
        table={"types": TABLE_LIKE_TYPES},
        x=table_selection_gui_option("table"),
        y=table_selection_gui_option("table"),
        weights=table_selection_gui_option("table"),
        initial_params={"types": Types.PARAMS},
        method={"choices": MINIMZE_METHODS},
    )
    def curve_fit_values(
        table: SubWindow,
        x: SelectionType,
        y: SelectionType,
        weights: SelectionType | None = None,
        initial_params: WidgetDataModel | None = None,
        method: str = "leastsq",
    ) -> WidgetDataModel:
        """Curve fit"""
        model_table = table.to_model()
        xarr, yarr = _model_to_xy(model_table, x, y)
        if weights is not None:
            weightsarr = _model_to_xy(model_table, x, weights)[1].array
        else:
            weightsarr = None
        if initial_params is None:
            params = None
        else:
            params = initial_params.value
        result = lmfit_model.fit(
            yarr.array,
            params=params,
            weights=weightsarr,
            method=method,
            x=xarr.array,
        )
        return WidgetDataModel(
            value=result,
            type=Types.MODEL_RESULT,
            title=f"Curve fit of {model.title}",
        )

    return curve_fit_values


@register_function(
    menus=Menus.LMFIT_RESULTS,
    title="Fit report",
    types=[Types.MODEL_RESULT],
    command_id="himena_lmfit:fit:fit-report",
)
def fit_report(model: WidgetDataModel) -> WidgetDataModel:
    """Show the fit report"""
    minimizer = _cast_lmfit_model_result(model)
    report = minimizer.fit_report()
    return WidgetDataModel(
        value=report,
        type="text",
        title=f"Report of {model.title}",
    )


@register_function(
    menus=Menus.LMFIT_RESULTS,
    title="Confidence Interval Report",
    types=[Types.MODEL_RESULT],
    command_id="himena_lmfit:fit:ci-report",
)
def ci_report(model: WidgetDataModel) -> WidgetDataModel:
    """Generate confidence interval report"""
    minimizer = _cast_lmfit_model_result(model)
    report = minimizer.ci_report()
    return WidgetDataModel(
        value=report,
        type="text",
        title=f"CI Report of {model.title}",
    )


@register_function(
    menus=Menus.LMFIT_RESULTS,
    title="Plot fit result",
    types=[Types.MODEL_RESULT],
    command_id="himena_lmfit:fit:plot-fit-result",
)
def plot_fit_result(model: WidgetDataModel) -> WidgetDataModel:
    """Plot the fit result"""
    minimizer = _cast_lmfit_model_result(model)
    fig = minimizer.plot()
    return create_model(
        fig,
        type=StandardType.MPL_FIGURE,
        title=f"Plot of {model.title}",
    )


def _cast_lmfit_model(model: WidgetDataModel) -> "lmfit.Model":
    """Cast to lmfit model"""
    if model.is_subtype_of(StandardType.FUNCTION):
        return lmfit.Model(model.value)
    elif isinstance(model.value, lmfit.Model):
        return model.value
    raise TypeError("model must be of type lmfit.Model")


def _cast_lmfit_model_result(model: WidgetDataModel) -> "lmfit.model.ModelResult":
    """Cast to lmfit model"""
    if not isinstance(model.value, lmfit.model.ModelResult):
        raise TypeError("model must be of type lmfit.model.ModelResult")
    return model.value
