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

    if countries is None:
        cases_countries = df_cases.loc[:, '1/22/20':].transpose(copy=True)
        countries_columns = df_cases.loc[:, 'Country/Region'].tolist()
    else:
        # get the rows matching the countries and the columns from the first known datastamp
        # transpose it so that the countries are the columns
        cases_countries = df_cases[df_cases['Country/Region'].isin(countries)].loc[:, '1/22/20':].transpose(copy=True)
        # reset the name of the columns as the countries
        countries_columns = df_cases[df_cases['Country/Region'].isin(countries)].loc[:, 'Country/Region'].tolist()

    cases_countries.columns = countries_columns

    # replace the date string as index with the day of the year (useful if later on we need to compute models)
    days = dt.str_to_day_of_year(cases_countries.index.to_list())
    cases_countries.index = days

    return cases_countries

