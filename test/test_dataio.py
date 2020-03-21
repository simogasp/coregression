import unittest
import mytools.dataio as io


class TesterItaly(unittest.TestCase):

    def setUp(self):
        self.regions_of_italy = ['Abruzzo', 'Basilicata', 'P.A. Bolzano', 'Calabria', 'Campania', 'Emilia Romagna',
                                 'Friuli Venezia Giulia', 'Lazio', 'Liguria', 'Lombardia', 'Marche', 'Molise',
                                 'Piemonte', 'Puglia', 'Sardegna', 'Sicilia', 'Toscana', 'P.A. Trento', 'Umbria',
                                 "Valle d'Aosta", 'Veneto']
        self.provinces_veneto = ['Verona', 'Vicenza', 'Padova', 'Rovigo', 'Venezia', 'Treviso', 'Belluno']
        self.provinces_veneto.sort()

    def test_provinces_of_regions(self):
        provinces = io.italy_get_list_of_provinces_for_region('Veneto')
        self.assertListEqual(provinces, self.provinces_veneto)

    def test_provinces_of_italy(self):
        self.assertListEqual(io.italy_get_list_of_regions(), self.regions_of_italy)


if __name__ == '__main__':
    unittest.main()
