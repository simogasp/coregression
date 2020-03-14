from typing import List
import pandas as pd
import mytools.date as dt


def get_filename_confirmed_cases() -> str:
    return 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data' \
           '/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'


def get_filename_death_cases() -> str:
    return 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data' \
              '/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'


def get_filename_recovered_cases() -> str:
    return 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data' \
                 '/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'


def load_cases(file_name: str, countries: List[str]=None) -> pd.DataFrame:
    df_cases = pd.read_csv(file_name)

    first_date = '1/22/20'
    country_col = 'Country/Region'
    province_col = 'Province/State'

    if countries is None:
        cases_countries = df_cases.loc[:, first_date:].transpose(copy=True)
        countries_columns = df_cases.loc[:, country_col].tolist()
    else:
        # get the rows matching the countries and the columns from the first known datastamp

        # for some countries multiple items are available if regional data is available.
        # if the region has no regional data the province is empty
        # otherwise it has the name of the region or the name of the country for the country overall stats
        condition = ((df_cases[province_col].isin(countries) | pd.isna(df_cases[province_col]) ) & df_cases[country_col].isin(countries))
        # transpose it so that the countries are the columns
        cases_countries = df_cases[condition].loc[:, first_date:].transpose(copy=True)
        # reset the name of the columns as the countries
        countries_columns = df_cases[condition].loc[:, country_col].tolist()

    cases_countries.columns = countries_columns

    # replace the date string as index with the day of the year (useful if later on we need to compute models)
    days = dt.str_to_day_of_year(cases_countries.index.to_list())
    cases_countries.index = days

    return cases_countries

