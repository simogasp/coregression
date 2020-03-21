from typing import List, Union
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
    dates = dt.str_convert_mdy_to_dmy(cases_countries.index.to_list())
    cases_countries.index = dates

    return cases_countries


# ITALY

italy_region_name_field = 'denominazione_regione'
italy_province_name_field = 'denominazione_provincia'
italy_not_a_province = 'In fase di definizione/aggiornamento'
italy_date_field = 'data'


def italy_get_filename_regions() -> str:
    return 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv'


def italy_get_filename_provinces() -> str:
    return 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv'


def italy_load(file_name: str, field: str, search_for: List[str] = None) -> pd.DataFrame:
    df_cases = pd.read_csv(file_name)

    dates = dt.str_convert_date(df_cases[italy_date_field].tolist(), format_from=dt.format_ISO8601,
                                format_to=dt.format_ddmmyy)
    df_cases.index = dates

    if search_for is None:
        return df_cases

    return df_cases[df_cases[field].isin(search_for)].drop(columns=italy_date_field)


def italy_load_provinces(file_name: str, provinces: List[str] = None) -> pd.DataFrame:
    return italy_load(file_name, italy_province_name_field, provinces)


def italy_load_regions(file_name: str, regions: List[str] = None) -> pd.DataFrame:
    return italy_load(file_name, italy_region_name_field, regions)


def italy_filter_by_category(data_frame: pd.DataFrame, field: str, category: str) -> pd.DataFrame:
    filtered = pd.DataFrame(data_frame[[field, category]])

    regions = filtered[field].unique().tolist()

    data = {}
    days = filtered.index.unique().tolist()

    for reg in regions:
        data[reg] = filtered[filtered[field] == reg][category].tolist()

    return pd.DataFrame(data, index=days)


def italy_regions_filter_by_category(data_frame: pd.DataFrame, category: str) -> pd.DataFrame:
    return italy_filter_by_category(data_frame, field=italy_region_name_field, category=category)


def italy_provinces_filter_by_category(data_frame: pd.DataFrame, category: str) -> pd.DataFrame:
    return italy_filter_by_category(data_frame, field=italy_province_name_field, category=category)


def italy_get_list_of_provinces_for_region(region: str) -> List[str]:
    df_cases = pd.read_csv(italy_get_filename_provinces())
    # exclude the non province
    condition = (df_cases[italy_region_name_field] == region) & (df_cases[italy_province_name_field] != italy_not_a_province)
    return df_cases[condition][italy_province_name_field].unique().tolist()
