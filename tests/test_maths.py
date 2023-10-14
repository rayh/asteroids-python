from cmath import pi
from asteroids.maths import diff_angle

def test_diff_between_angles():
    assert diff_angle(0, 0) == 0
    assert diff_angle(0, pi) == pi
    assert diff_angle(0, 3/2 * pi) == pi/2
    assert diff_angle(3/2 * pi, 0) == -pi/2
    assert diff_angle(2*pi, 2*pi) == 0
    assert diff_angle(2*pi, pi/2) == -pi/2
    assert diff_angle(2*pi, 2.5*pi) == -pi/2