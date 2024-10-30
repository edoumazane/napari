from vispy.scene.visuals import Compound, Rectangle, Text


class LayersInfoBox(Compound):
    def __init__(self) -> None:
        self._layer_names = [
            'layer_1',
        ]
        self._nlayers = len(self._layer_names)
        self._default_color = [1.0, 1.0, 1.0, 1.0]
        self.colors = [
            self._default_color,
        ]
        self._box_default_color = [0.0, 0.0, 0.0, 0.0]
        self.box_color = self._box_default_color
        self.position = 'bottom_left'

        # order matters (last is drawn on top)
        super().__init__(
            [
                Rectangle(
                    center=[0.5, 0.5],
                    width=1.1,
                    height=36,
                    color=self.box_color,
                ),
                Text(
                    text='1px',
                    pos=[0.5, 0.5],
                    anchor_x='left',
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

    def set_layer_names(self):
        layer_names = self._layer_names
        self._nlayers = len(layer_names)
        self.colors = [self._default_color] * self._nlayers
        self.text.text = '\n'.join(layer_names)
        self.text.color = (
            self.colors[0] if self.colors else self._default_color
        )

        # self.text.color = np.mean(np.array(self.colors), axis=1) if self.colors else self._default_color
        # self.box.color = 1 - self.text.color
