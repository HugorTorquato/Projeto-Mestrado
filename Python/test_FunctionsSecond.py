import unittest
from FunctionsSecond import Min_2


class Test(unittest.TestCase):
    def test_min_2(self):
        # Assume
        vet = [0, 0, 0, 0, 0.5]
        validate = True

        # Act
        vet2 = Min_2(vet)

        for number in vet2:
            if number == 0:
                validate = False

        #Assert
        self.assertTrue(validate)
