import unittest
import mytools.dataio as io


class TesterItaly(unittest.TestCase):

    def setUp(self):
        self.provinces_veneto = ['Verona', 'Vicenza', 'Padova', 'Rovigo', 'Venezia', 'Treviso', 'Belluno']
        self.provinces_veneto.sort()

    def test_provinces_of_regions(self):
        provinces = io.italy_get_list_of_provinces_for_region('Veneto')
        self.assertListEqual(provinces, self.provinces_veneto)


if __name__ == '__main__':
    unittest.main()
