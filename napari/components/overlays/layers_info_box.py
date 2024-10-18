"""Layers info box model."""

from napari._pydantic_compat import Field
from napari.components.overlays.base import CanvasOverlay
from napari.utils.color import ColorValue


class LayersInfoBoxOverlay(CanvasOverlay):
    """Info box indicating a list of the names of visible layers.

    Attributes
    ----------
    color : ColorValue
        Text color.
        See ``ColorValue.validate`` for supported values.
    background_color : np.ndarray
        Background color of canvas. If scale bar is not colored
        then it has the color opposite of this color.
    font_size : float
        The font size (in points) of the text.
    box : bool
        If background box is visible or not.
    box_color : Optional[str | array-like]
        Background box color.
        See ``ColorValue.validate`` for supported values.
    position : CanvasPosition
        The position of the overlay in the canvas.
    visible : bool
        If the overlay is visible or not.
    opacity : float
        The opacity of the overlay. 0 is fully transparent.
    order : int
        The rendering order of the overlay: lower numbers get rendered first.
    """

    colored: bool = False
    color: ColorValue = Field(default_factory=lambda: ColorValue([1, 0, 1, 1]))
    font_size: float = 10
    box: bool = False
    box_color: ColorValue = Field(
        default_factory=lambda: ColorValue([0, 0, 0, 0.6])
    )
