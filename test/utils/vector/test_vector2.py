from unittest import TestCase

from utils.vector import Vector2


class TestVector2(TestCase):

    def test_vector_from_tuple(self):
        v = Vector2((2,2))
        self.assertTupleEqual(v.pt,(2,2))

    def test_vector_from_args(self):
        v = Vector2(3, 4)
        self.assertTupleEqual(v.pt, (3, 4))

    def test_zero_vector(self):
        v = Vector2()
        self.assertTupleEqual(v.pt, (0, 0))

    def test_scalar_add(self):
        v = Vector2(2, 2)
        self.assertEqual(v+4, (6, 6))

    def test_vector_add(self):
        v1, v2 = Vector2(2, 2), Vector2(3, 4)
        self.assertEqual(v1+v2, (5, 6))

    def test_scalar_mult(self):
        v = Vector2(4,4)
        self.assertEqual(v * 3, (12, 12))

    def test_in_bounds(self):
        v, v_max = Vector2(3,2), Vector2(5,5)
        self.assertTrue(0 <= v < v_max)

    def test_out_of_bounds(self):
        v, v_max = Vector2(3, 7), Vector2(5, 5)
        self.assertFalse(0 <= v < v_max)