import unittest
import mytools.date as dt
import datetime


class MyTestCase(unittest.TestCase):

    def test_day_of_year_to_date(self):
        year = 2011
        this_year = int(datetime.datetime.now().year)
        date_list = [datetime.datetime(year, 1, 1, 0), datetime.datetime(year, 2, 1, 0), datetime.datetime(year, 2, 4, 0)]
        date_list_this_year = [datetime.datetime(this_year, 1, 1, 0), datetime.datetime(this_year, 2, 1, 0), datetime.datetime(this_year, 2, 4, 0)]
        days_list = [1, 32, 35]
        self.assertEqual(dt.day_of_year_to_date(days_list[0], year), date_list[0])
        self.assertEqual(dt.day_of_year_to_date(days_list[1], year), date_list[1])
        self.assertEqual(dt.day_of_year_to_date(days_list[2], year), date_list[2])
        self.assertListEqual(dt.day_of_year_to_date(days_list, year), date_list)
        self.assertListEqual(dt.day_of_year_to_date(days_list), date_list_this_year)


if __name__ == '__main__':
    unittest.main()
