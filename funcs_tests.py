import unittest
from funcs import *

class Tests(unittest.TestCase):
   def test_transpose_1(self):
      matrix = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
      transposed_matrix = [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
      self.assertEqual(transpose(matrix), transposed_matrix)

   def test_transpose_2(self):
      matrix = [[0]]
      transposed_matrix = [[0]]
      self.assertEqual(transpose(matrix), transposed_matrix)

   def test_transpose_3(self):
      matrix = [[55.0, 77.6, 200]]
      transposed_matrix = [[55.0], [77.6], [200]]
      self.assertEqual(transpose(matrix), transposed_matrix)

   def test_transpose_4(self):
      matrix = [[100.0, 0.01, 3.4], [200.0, 0.03, 4.9], [300.0, 0.05, 5.7], [400.0, 0.07, 6.3]]
      transposed_matrix = [[100.0, 200.0, 300.0, 400.0], [0.01, 0.03, 0.05, 0.07], [3.4, 4.9, 5.7, 6.3]]
      self.assertEqual(transpose(matrix), transposed_matrix)

   def test_transpose_5(self):
      matrix = [[1.0], [2.0], [3.0], [1000.0]]
      transposed_matrix = [[1.0, 2.0, 3.0, 1000.0]]
      self.assertEqual(transpose(matrix), transposed_matrix)

   def test_objectify_1(self):
      data = [['105x45', [[1000.0, 0.03, 0.0, 0.02, 0.03, 0.08], [2000.0, 0.13, 0.0, 0.08, 0.03, 0.08]]],
              ['9x8E-3', [[1000.0, 0.04, 0.0, 0.04, 0.12, 0.21], [2000.0, 0.18, 0.0, 0.14, 0.12, 0.21]]]]
      propellers_list = objectify(data)

      self.assertEqual(propellers_list[0].name, '105x45')
      self.assertEqual(propellers_list[0].rpm_list, [1000.0, 2000.0])
      self.assertEqual(propellers_list[0].thrust_list, [0.03, 0.13])
      self.assertEqual(propellers_list[0].power_list, [0.0, 0.0])
      self.assertEqual(propellers_list[0].torque_list, [0.02, 0.08])
      self.assertEqual(propellers_list[0].cp_list, [0.03, 0.03])
      self.assertEqual(propellers_list[0].ct_list, [0.08, 0.08])

      self.assertEqual(propellers_list[1].name, '9x8E-3')
      self.assertEqual(propellers_list[1].rpm_list, [1000.0, 2000.0])
      self.assertEqual(propellers_list[1].thrust_list, [0.04, 0.18])
      self.assertEqual(propellers_list[1].power_list, [0.0, 0.0])
      self.assertEqual(propellers_list[1].torque_list, [0.04, 0.14])
      self.assertEqual(propellers_list[1].cp_list, [0.12, 0.12])
      self.assertEqual(propellers_list[1].ct_list, [0.21, 0.21])