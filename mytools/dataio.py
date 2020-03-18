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


def load_cases(file_name: str, countries: List[str] = None) -> pd.DataFrame:
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
        condition = ((df_cases[province_col].isin(countries) | pd.isna(df_cases[province_col])) & df_cases[
            country_col].isin(countries))
        # transpose it so that the countries are the columns
        cases_countries = df_cases[condition].loc[:, first_date:].transpose(copy=True)
        # reset the name of the columns as the countries
        countries_columns = df_cases[condition].loc[:, country_col].tolist()

    cases_countries.columns = countries_columns

    # replace the date string as index with the day of the year (useful if later on we need to compute models)
    days = dt.str_to_day_of_year(cases_countries.index.to_list())
    cases_countries.index = days

    return cases_countries


# ITALY

def italy_get_filename_regions() -> str:
    return 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv'


def italy_get_filename_provinces() -> str:
    return 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv'


def italy_load_regions(file_name: str, regions: List[str] = None) -> pd.DataFrame:
    df_cases = pd.read_csv(file_name)

    data_col = 'data'
    df_cases[data_col] = dt.str_to_day_of_year(df_cases[data_col].tolist(), '%Y-%m-%d %H:%M:%S')

    if regions is None:
        return df_cases

    region_col = 'denominazione_regione'
    return df_cases[df_cases[region_col].isin(regions)]


def italy_regions_filter_by_category(data_frame: pd.DataFrame, category: str) -> pd.DataFrame:
    region_col = 'denominazione_regione'
    data_col = 'data'
    day_col = 'day'
    filtered = pd.DataFrame(data_frame[[data_col, region_col, category]])

    regions = filtered[region_col].unique().tolist()

    data = {day_col: filtered[data_col].unique().tolist()}

    for reg in regions:
        data[reg] = filtered[filtered[region_col] == reg][category].tolist()

    return pd.DataFrame(data)