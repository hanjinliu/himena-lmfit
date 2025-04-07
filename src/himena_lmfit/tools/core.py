from himena import Parametric, WidgetDataModel, StandardType, create_model
from himena.widgets import SubWindow
from himena.data_wrappers import wrap_dataframe, DataFrameWrapper
from himena.standards import plotting as hplt
from himena.standards.plotting.models import PlotModelXY
from himena.utils.table_selection import (
    table_selection_gui_option,
    model_to_xy_arrays,
    TABLE_LIKE_TYPES,
)
from himena_builtins.tools.conversions import table_to_dataframe
from himena.plugins import register_function, configure_gui
import numpy as np
from himena_lmfit._lazy_import import lmfit
from himena_lmfit._magicgui import ParamEdit
from himena_lmfit.consts import Menus, Types, MINIMZE_METHODS

SelectionType = tuple[tuple[int, int], tuple[int, int]]


def _model_to_xy(model, x, y):
    xout, youts = model_to_xy_arrays(
        model, x, y, allow_empty_x=False, allow_multiple_y=False
    )
    return xout.array, youts[0].array


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
        params = lmfit_model.guess(yarr, xarr)
        return WidgetDataModel(
            value=params,
            type=Types.PARAMS,
            title=f"Guessed Parameters of {model.title}",
        )

    return guess_param_values


@register_function(
    menus=["tools/lmfit/optimize", "/model_menu/lmfit"],
    title="Guess parameters",
    types=[StandardType.TABLE, StandardType.DATAFRAME, StandardType.PLOT],
    command_id="himena_lmfit:models:guess-params-from-table",
)
def guess_params_from_table(model: WidgetDataModel) -> Parametric:
    """Guess parameters from table data"""

    @configure_gui(
        function={"types": [StandardType.FUNCTION, Types.MODEL]},
    )
    def guess_param_values(function: WidgetDataModel) -> WidgetDataModel:
        """Guess parameters"""
        lmfit_model = _cast_lmfit_model(function)
        df = _to_dataframe(model)
        cols = df.column_names()
        if len(cols) != 2:
            raise ValueError("DataFrame must have exactly 2 columns")
        params = lmfit_model.guess(df[cols[1]], df[cols[0]])
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
        guess: bool = True,
        method: str = "leastsq",
    ) -> WidgetDataModel:
        """Curve fit"""
        model_table = table.to_model()
        xarr, yarr = _model_to_xy(model_table, x, y)
        if weights is not None:
            weightsarr = _model_to_xy(model_table, x, weights)[1]
        else:
            weightsarr = None
        if initial_params is None:
            if guess:
                params = lmfit_model.guess(yarr, xarr)
            else:
                params = None
        else:
            params = initial_params.value
        result = lmfit_model.fit(
            yarr,
            params=params,
            weights=weightsarr,
            method=method,
            x=xarr,
        )
        return WidgetDataModel(
            value=result,
            type=Types.MODEL_RESULT,
            title=f"Curve fit of {model.title}",
        )

    return curve_fit_values


@register_function(
    menus=["tools/lmfit/optimize", "/model_menu/lmfit"],
    title="Curve fit ...",
    types=[StandardType.TABLE, StandardType.DATAFRAME, StandardType.PLOT],
    command_id="himena_lmfit:fit:curve-fit-from-table",
)
def curve_fit_from_table(model: WidgetDataModel) -> Parametric:
    """Curve fit from table data"""

    @configure_gui(
        function={"types": [StandardType.FUNCTION, Types.MODEL]},
        initial_params={"types": Types.PARAMS},
        method={"choices": MINIMZE_METHODS},
    )
    def curve_fit_values(
        function: WidgetDataModel,
        initial_params: WidgetDataModel | None = None,
        guess: bool = True,
        method: str = "leastsq",
    ) -> WidgetDataModel:
        """Curve fit"""
        lmfit_model = _cast_lmfit_model(function)
        df = _to_dataframe(model)
        cols = df.column_names()
        if len(cols) == 2:
            xarr = df[cols[0]]
            yarr = df[cols[1]]
            weightsarr = None
        elif len(cols) == 3:
            xarr = df[cols[0]]
            yarr = df[cols[1]]
            weightsarr = df[cols[2]]
        else:
            raise ValueError("DataFrame must have exactly 2 columns")

        if initial_params is None:
            if guess:
                params = lmfit_model.guess(yarr, xarr)
            else:
                params = None
        else:
            params = initial_params.value
        result = lmfit_model.fit(
            yarr,
            params=params,
            weights=weightsarr,
            method=method,
            x=xarr,
        )
        return WidgetDataModel(
            value=result,
            type=Types.MODEL_RESULT,
            title=f"Curve fit of {model.title}",
        )

    return curve_fit_values


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
    keybindings=["P"],
)
def plot_fit_result(model: WidgetDataModel) -> WidgetDataModel:
    """Plot the fit result"""
    minimizer = _cast_lmfit_model_result(model)
    fig = hplt.figure()

    independent_var = _independent_var(minimizer)
    x_array = minimizer.userkws[independent_var]
    x_array_dense = np.linspace(min(x_array), max(x_array), 256)
    fig.scatter(x_array, minimizer.data, color="gray", name="data")

    y_eval = minimizer.model.eval(minimizer.params, **{independent_var: x_array_dense})
    if isinstance(
        minimizer.model, (lmfit.models.ConstantModel, lmfit.models.ComplexConstantModel)
    ):
        y_eval *= np.ones(x_array_dense.size)

    fig.plot(x_array_dense, y_eval, color="red", name="fit")

    fig.axes.x.label = independent_var
    fig.axes.y.label = "y"
    return create_model(
        fig,
        type=StandardType.PLOT,
        title=f"Plot of {model.title}",
    )


@register_function(
    menus=Menus.LMFIT_RESULTS,
    title="Plot fit result",
    types=[Types.MODEL_RESULT],
    command_id="himena_lmfit:fit:plot-fit-residual",
    keybindings=["R"],
)
def plot_fit_residual(model: WidgetDataModel) -> WidgetDataModel:
    """Plot the fit result"""
    minimizer = _cast_lmfit_model_result(model)
    fig = hplt.figure()
    independent_var = _independent_var(minimizer)
    x_array = minimizer.userkws[independent_var]

    fig.plot([x_array.min(), x_array.max()], [0, 0], color="black", style="--")

    y_eval = minimizer.model.eval(minimizer.params, **{independent_var: x_array})
    if isinstance(
        minimizer.model, (lmfit.models.ConstantModel, lmfit.models.ComplexConstantModel)
    ):
        y_eval *= np.ones(x_array.size)

    residuals = minimizer.data - minimizer.eval()
    fig.scatter(x_array, residuals, color="gray", name="residuals")

    fig.axes.y.label = "residuals"
    return create_model(
        fig,
        type=StandardType.PLOT,
        title=f"Residuals of {model.title}",
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


def _to_dataframe(model: WidgetDataModel) -> DataFrameWrapper:
    """Convert to DataFrame"""
    if model.is_subtype_of(StandardType.DATAFRAME):
        return wrap_dataframe(model.value)
    elif model.is_subtype_of(StandardType.TABLE):
        return wrap_dataframe(table_to_dataframe(model).value)
    elif model.is_subtype_of(StandardType.PLOT):
        if isinstance(axes := model.value, hplt.SingleAxes):
            if isinstance(plot := axes.axes.models[0], PlotModelXY):
                xname = axes.axes.x.label or "x"
                yname = axes.axes.y.label or "y"
                if yname == xname:
                    yname = yname = "_0"
                return wrap_dataframe({xname: plot.x, yname: plot.y})
        raise ValueError("Plot must contain a single XY plot")
    else:
        raise ValueError("Could not convert to DataFrame")


def _independent_var(minimizer: "lmfit.model.ModelResult") -> str:
    if len(minimizer.model.independent_vars) == 1:
        return minimizer.model.independent_vars[0]
    else:
        raise ValueError("Model must have exactly one independent variable")
