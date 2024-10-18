import numpy as np
from vispy.scene.visuals import Compound, Rectangle, Text


class LayersInfoBox(Compound):
    def __init__(self) -> None:
        self._data = np.array(
            [
                'layer_1',
                'layer_2',
            ]
        )

        # order matters (last is drawn on top)
        super().__init__(
            [
                Rectangle(center=[3.5, 0.5], width=1.1, height=36),
                Text(
                    text='1px',
                    pos=[3.5, 0.5],
                    anchor_x='center',
                    anchor_y='top',
                    font_size=10,
                ),
            ]
        )

    @property
    def text(self):
        return self._subvisuals[1]

    @property
    def box(self):
        return self._subvisuals[0]

    def set_text(self, color):
        data = self._data
        self.text.text = '\n'.join(data)
        self.text.color = color
