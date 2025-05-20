import numpy as np


class Object3D:
    def __init__(
        self,
        position=None,
        bounding_box_size=None,
    ):
        self.position = np.array(
            position if position is not None else [0.0, 0.0, 0.0], dtype=float
        )

        self.bounding_box_size = (
            bounding_box_size
            if bounding_box_size is not None
            else [np.array([-0.5, 0, -0.5]), np.array([0.5, 1, 0.5])]
        )

    def set_position(self, position):
        self.position = np.array(position, dtype=float)
