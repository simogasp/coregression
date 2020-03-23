from typing import List, Union
import pandas as pd
import mytools.date as dt

world_country_name_field = 'Country/Region'
world_province_name_field = 'Province/State'
world_first_date = '1/22/20'


def get_filename_confirmed_cases() -> str:
    return 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data' \
           '/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'


def get_filename_death_cases() -> str:
    return 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data' \
           '/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'


def get_filename_recovered_cases() -> str:
    return 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data' \
           '/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'


def world_load_cases(file_name: str, countries: List[str] = None) -> pd.DataFrame:
    df_cases = pd.read_csv(file_name)

    first_date = world_first_date
    country_col = world_country_name_field
    province_col = world_province_name_field

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


def world_load_stats_country(country: str) -> pd.DataFrame:

    confirmed_cases = world_load_cases(get_filename_confirmed_cases(), [country])
    death_cases = world_load_cases(get_filename_death_cases(), [country])
    recovered_cases = world_load_cases(get_filename_recovered_cases(), [country])

    overall_stats = pd.concat([confirmed_cases, death_cases, recovered_cases], axis=1, sort=False)
    overall_stats.columns = ['confirmed', 'deaths', 'recovered']

    return overall_stats


# ITALY

italy_region_name_field = 'denominazione_regione'
italy_province_name_field = 'denominazione_provincia'
italy_not_a_province = 'In fase di definizione/aggiornamento'
italy_date_field = 'data'

italy_northern_regions = ['P.A. Bolzano', 'Emilia Romagna', 'Friuli Venezia Giulia', 'Liguria', 'Lombardia', 'Piemonte',
                          'P.A. Trento', "Valle d'Aosta", 'Veneto']
italy_central_regions = ['Lazio', 'Marche', 'Toscana', 'Umbria']
italy_southern_regions = ['Abruzzo', 'Campania', 'Basilicata', 'Calabria', 'Molise', 'Puglia']
italy_islands_regions = ['Sardegna', 'Sicilia']


def italy_get_filename_regions() -> str:
    return 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv'


def italy_get_filename_provinces() -> str:
    return 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv'


def italy_get_filename_country() -> str:
    return 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv'


def italy_load(file_name: str, field: str, search_for: List[str] = None) -> pd.DataFrame:
    df_cases = pd.read_csv(file_name)

    dates = dt.str_convert_date(df_cases[italy_date_field].tolist(), format_from=dt.format_ISO8601,
                                format_to=dt.format_ddmmyy)
    df_cases.index = dates

    if search_for is None:
        return df_cases

    return df_cases[df_cases[field].isin(search_for)].drop(columns=italy_date_field)


def italy_load_provinces(provinces: List[str] = None) -> pd.DataFrame:
    return italy_load(italy_get_filename_provinces(), italy_province_name_field, provinces)


def italy_load_regions(regions: List[str] = None) -> pd.DataFrame:
    return italy_load(italy_get_filename_regions(), italy_region_name_field, regions)


def italy_load_whole_country() -> pd.DataFrame:
    return italy_load(italy_get_filename_country(), field='', search_for=None)


def italy_filter_by_category(data_frame: pd.DataFrame, field: str, category: str) -> pd.DataFrame:
    filtered = pd.DataFrame(data_frame[[field, category]])

    regions = filtered[field].unique().tolist()

    data = {}
    days = filtered.index.unique().tolist()

    for reg in regions:
        data[reg] = filtered[filtered[field] == reg][category].tolist()

    return pd.DataFrame(data, index=days)


def italy_country_filter_by_category(data_frame: pd.DataFrame, categories: List[str]) -> pd.DataFrame:
    return pd.DataFrame(data_frame[categories])


def italy_regions_filter_by_category(data_frame: pd.DataFrame, category: str) -> pd.DataFrame:
    return italy_filter_by_category(data_frame, field=italy_region_name_field, category=category)


def italy_provinces_filter_by_category(data_frame: pd.DataFrame, category: str) -> pd.DataFrame:
    return italy_filter_by_category(data_frame, field=italy_province_name_field, category=category)


def italy_get_list_of_provinces_for_region(region: str) -> List[str]:
    df_cases = pd.read_csv(italy_get_filename_provinces())
    # exclude the non province
    condition = (df_cases[italy_region_name_field] == region) & (df_cases[italy_province_name_field] != italy_not_a_province)
    return df_cases[condition][italy_province_name_field].unique().tolist()


def italy_get_list_of_regions() -> List[str]:
    """
    Get the list of all italian regions
    Returns:
        the list of regions in Italy
    """
    return italy_load_regions()[italy_region_name_field].unique().tolist()
