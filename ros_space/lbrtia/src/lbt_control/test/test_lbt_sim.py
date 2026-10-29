import math

import numpy as np

from lbt_control.lbt_sim import raycast


def test_raycast_hits_nearest_box_and_misses_to_inf():
    boxes = np.array([[1.0, 1.1, -1.0, 1.0],    # pared vertical en x=1
                      [3.0, 3.1, -1.0, 1.0]])   # otra detrás
    r = raycast(boxes, 0.0, 0.0, np.array([0.0, math.pi, math.pi / 2]))
    assert math.isclose(r[0], 1.0)
    assert math.isinf(r[1]) and math.isinf(r[2])


def test_raycast_beyond_range_max_is_inf():
    boxes = np.array([[10.0, 10.1, -1.0, 1.0]])
    assert math.isinf(raycast(boxes, 0.0, 0.0, np.array([0.0]))[0])
