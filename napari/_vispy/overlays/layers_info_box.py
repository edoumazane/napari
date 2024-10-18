import numpy as np
import pint

from napari._vispy.overlays.base import ViewerOverlayMixin, VispyCanvasOverlay
from napari._vispy.visuals.layers_info_box import LayersInfoBox
from napari.utils.colormaps.standardize_color import transform_color
from napari.utils.theme import get_theme


class LayersInfoBoxOverlay(ViewerOverlayMixin, VispyCanvasOverlay):
    """Info box indicating a list of the names of visible layers."""

    def __init__(self, *, viewer, overlay, parent=None) -> None:
        self._target_length = 150.0
        self._scale = 1
        self._unit: pint.Unit

        super().__init__(
            node=LayersInfoBox(), viewer=viewer, overlay=overlay, parent=parent
        )
        self.x_size = 150  # will be updated on zoom anyways
        # need to change from defaults because the anchor is in the center
        self.y_offset = 20
        self.y_size = 5

        self.overlay.events.box.connect(self._on_box_change)
        self.overlay.events.box_color.connect(self._on_data_change)
        self.overlay.events.color.connect(self._on_data_change)
        self.overlay.events.colored.connect(self._on_data_change)
        self.overlay.events.font_size.connect(self._on_text_change)
        self.overlay.events.ticks.connect(self._on_data_change)
        self.overlay.events.unit.connect(self._on_unit_change)
        self.overlay.events.length.connect(self._on_length_change)

        self.viewer.events.theme.connect(self._on_data_change)
        self.viewer.camera.events.zoom.connect(self._on_zoom_change)

        self.reset()

    def _on_zoom_change(self, *, force: bool = False):
        """Update axes length based on zoom scale."""

        # If scale has not changed, do not redraw
        scale = 1 / self.viewer.camera.zoom
        if abs(np.log10(self._scale) - np.log10(scale)) < 1e-4 and not force:
            return
        self._scale = scale

        scale_canvas2world = self._scale
        target_canvas_pixels = self._target_length
        # convert desired length to world size
        target_world_pixels = scale_canvas2world * target_canvas_pixels

        # If length is set, use that value to calculate the scale bar length
        if self.overlay.length is not None:
            target_canvas_pixels = self.overlay.length / scale_canvas2world
            new_dim = self.overlay.length * self._unit.units
        else:
            # calculate the desired length as well as update the value and units
            target_world_pixels_rounded, new_dim = self._calculate_best_length(
                target_world_pixels
            )
            target_canvas_pixels = (
                target_world_pixels_rounded / scale_canvas2world
            )

        scale = target_canvas_pixels

        # Update scalebar and text
        self.node.transform.scale = [scale, 1, 1, 1]
        self.node.text.text = f'{new_dim:g~#P}'
        self.x_size = scale  # needed to offset properly
        self._on_position_change()

    def _on_data_change(self):
        """Change color and data of scale bar and box."""
        color = self.overlay.color
        box_color = self.overlay.box_color

        if not self.overlay.colored:
            if self.overlay.box:
                # The box is visible - set the scale bar color to the negative of the
                # box color.
                color = 1 - box_color
                color[-1] = 1
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

        self.node.set_data(color, self.overlay.ticks)
        self.node.box.color = box_color

    def _on_box_change(self):
        self.node.box.visible = self.overlay.box

    def _on_text_change(self):
        """Update text information"""
        self.node.text.font_size = self.overlay.font_size

    def reset(self):
        super().reset()
        self._on_data_change()
        self._on_box_change()
        self._on_text_change()
        self._on_length_change()
