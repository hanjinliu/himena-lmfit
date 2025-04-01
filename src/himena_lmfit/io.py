from pathlib import Path
from himena.plugins import register_reader_plugin, register_writer_plugin
from himena import WidgetDataModel, create_model

from himena_lmfit._lazy_import import lmfit
from himena_lmfit.consts import Types


@register_reader_plugin
def read_lmfit_model(path: Path) -> "lmfit.Model":
    """Read a lmfit model from a file."""
    model = lmfit.model.load_model(path)
    if not isinstance(model, lmfit.Model):
        raise TypeError("model must be of type lmfit.Model")
    return create_model(model, type=Types.MODEL)


@read_lmfit_model.define_matcher
def _match_lmfit_model(path: Path) -> str:
    if path.suffix == ".json":
        return Types.MODEL
    return None


@register_writer_plugin
def write_lmfit_model(model: WidgetDataModel, path: Path) -> None:
    """Write a lmfit model to a file."""
    if not isinstance(model.value, lmfit.Model):
        raise TypeError("model must be of type lmfit.Model")
    lmfit.model.save_model(model.value, path)
    return None


@write_lmfit_model.define_matcher
def _match_lmfit_model_write(model: WidgetDataModel, path: Path) -> bool:
    """Check if the model is a lmfit model."""
    return isinstance(model.value, lmfit.Model)


@register_reader_plugin
def read_lmfit_result(path: Path) -> "lmfit.model.ModelResult":
    """Read a lmfit result from a file."""
    result = lmfit.model.load_modelresult(path)
    if not isinstance(result, lmfit.model.ModelResult):
        raise TypeError("result must be of type lmfit.ModelResult")
    return create_model(result, type=Types.MODEL_RESULT)


@read_lmfit_result.define_matcher
def _match_lmfit_result(path: Path) -> str:
    if path.suffix == ".json":
        return Types.MODEL_RESULT
    return None


@register_writer_plugin
def write_lmfit_result(model: WidgetDataModel, path: Path) -> None:
    """Write a lmfit result to a file."""
    if not isinstance(model.value, lmfit.model.ModelResult):
        raise TypeError("model must be of type lmfit.model.ModelResult")
    lmfit.model.save_modelresult(model.value, path)
    return None


@write_lmfit_result.define_matcher
def _match_lmfit_result_write(model: WidgetDataModel, path: Path) -> bool:
    """Check if the model is a lmfit result."""
    return isinstance(model.value, lmfit.model.ModelResult)
