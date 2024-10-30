import numpy as np

from napari._vispy.overlays.base import ViewerOverlayMixin, VispyCanvasOverlay
from napari._vispy.visuals.layers_info_box import LayersInfoBox
from napari.utils.colormaps.standardize_color import transform_color
from napari.utils.theme import get_theme


class VispyLayersInfoBoxOverlay(ViewerOverlayMixin, VispyCanvasOverlay):
    """Info box indicating a list of the names of visible layers."""

    def __init__(self, *, viewer, overlay, parent=None) -> None:
        self._scale = 1

        super().__init__(
            node=LayersInfoBox(), viewer=viewer, overlay=overlay, parent=parent
        )
        self.x_size = 150  # will be updated on zoom anyways
        # need to change from defaults because the anchor is in the center
        self.y_offset = 20
        self.y_size = 5

        self.overlay.events.box.connect(self._on_box_change)
        self.overlay.events.box_color.connect(self._on_text_change)
        self.overlay.events.color.connect(self._on_text_change)
        self.overlay.events.colored.connect(self._on_text_change)
        self.overlay.events.font_size.connect(self._on_text_change)

        self.viewer.events.theme.connect(self._on_text_change)
        self.viewer.layers.events.connect(self._on_text_change)
        self.viewer.layers.events.connect(self._on_box_change)

        self.reset()

    def _on_data_change(self):
        """Change color and data of scale bar and box."""

    def _on_box_change(self):
        self.node.box.visible = self.overlay.box

        if self.overlay.box:
            colors = self.overlay.colors
            box_color = self.overlay.box_color

            if not self.overlay.colored:
                if self.overlay.box:
                    # The box is visible - set the text color to the negative of the
                    # box color.
                    colors = 1 - box_color
                    colors[-1] = 1
                else:
                    # set scale color negative of theme background.
                    # the reason for using the `as_hex` here is to avoid
                    # `UserWarning` which is emitted when RGB values are above 1
                    if (
                        self.node.parent is not None
                        and self.node.parent.canvas.bgcolor
                    ):
                        background_color = self.node.parent.canvas.bgcolor.rgba
                    else:
                        background_color = get_theme(
                            self.viewer.theme
                        ).canvas.as_hex()
                        background_color = transform_color(background_color)[0]
                    color = np.subtract(1, background_color)
                    color[-1] = background_color[-1]

            self.node.text.color = color
            self.node.box.color = box_color

    def _on_text_change(self):
        """Update text information"""
        self.node.text.font_size = self.overlay.font_size
        self.node._layer_names = [
            layer.name for layer in self.viewer.layers if layer.visible
        ][::-1]
        self.node.set_layer_names()

    def reset(self):
        super().reset()
        self._on_box_change()
        self._on_text_change()
