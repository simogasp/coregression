import unittest
import mytools.date as dt
import datetime


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.year = 2011
        self.format = '%d/%m/%y'
        self.this_year = int(datetime.datetime.now().year)
        self.date_list = [datetime.datetime(self.year, 1, 1, 0),
                          datetime.datetime(self.year, 2, 1, 0),
                          datetime.datetime(self.year, 2, 4, 0)]
        self.date_list_this_year = [datetime.datetime(self.this_year, 1, 1, 0),
                                    datetime.datetime(self.this_year, 2, 1, 0),
                                    datetime.datetime(self.this_year, 2, 4, 0)]
        self.days_list = [1, 32, 35]
        self.str_date_list = [d.strftime(self.format) for d in self.date_list]

    def test_day_of_year_to_date(self):
        self.assertEqual(dt.day_of_year_to_date(self.days_list[0], self.year), self.date_list[0])
        self.assertEqual(dt.day_of_year_to_date(self.days_list[1], self.year), self.date_list[1])
        self.assertEqual(dt.day_of_year_to_date(self.days_list[2], self.year), self.date_list[2])
        self.assertListEqual(dt.day_of_year_to_date(self.days_list, self.year), self.date_list)
        self.assertListEqual(dt.day_of_year_to_date(self.days_list), self.date_list_this_year)

    def test_date_to_day_of_year(self):
        self.assertEqual(dt.date_to_day_of_year(self.date_list[0]), self.days_list[0])
        self.assertEqual(dt.date_to_day_of_year(self.date_list[1]), self.days_list[1])
        self.assertEqual(dt.date_to_day_of_year(self.date_list[2]), self.days_list[2])
        self.assertListEqual(dt.date_to_day_of_year(self.date_list), self.days_list)

    def test_str_to_day_of_year(self):
        self.assertEqual(dt.str_to_day_of_year(self.str_date_list[0], self.format), self.days_list[0])
        self.assertEqual(dt.str_to_day_of_year(self.str_date_list[1], self.format), self.days_list[1])
        self.assertEqual(dt.str_to_day_of_year(self.str_date_list[2], self.format), self.days_list[2])
        self.assertListEqual(dt.str_to_day_of_year(self.str_date_list, self.format), self.days_list)


if __name__ == '__main__':
    unittest.main()
