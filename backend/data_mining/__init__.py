import logging
from datetime import datetime, timedelta
from functools import reduce

import geopandas as gpd
import numpy as np
import pandas as pd

from backend import models
from backend.application import db
from backend.application.settings import BackendSettings
from backend.data_mining import serializers
from backend.data_mining.service import COVID19API

logger = logging.getLogger(__name__)

# should be in appropriate format as an API documentation
DETAILED_COUNTRIES = ["china", "australia", "US", "canada"]
DETAILED_STATUSES = ["confirmed", "deaths", "recovered"]


def extract_world_data():
    world_json = COVID19API.get_world_total_cases()
    return serializers.WorldDataTotalSerializer.serialize_json_list(
        world_json, list_field_name="Countries"
    )


def get_yesterday():
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%dT%H:%M:%SZ")


def extract_detailed_countries_data(date_after=None):
    if not date_after:
        date_after = get_yesterday()

    countries_data_frames = []
    for country in DETAILED_COUNTRIES:
        status_data_frames = []

        for status in DETAILED_STATUSES:
            countries_json = COVID19API.get_details_for_country(
                country=country, status=status, date_after=date_after
            )
            serializer = serializers.SERIALIZER_STATUS_MAPPING[status]

            data_frame = serializer.serialize_json_list(countries_json)
            data_frame = data_frame.sort_values(
                by=f"cases_{status}", ascending=False
            ).drop_duplicates("province")

            if status == "confirmed":
                columns_to_use = ["country", "province", f"cases_{status}"]
            else:
                columns_to_use = ["province", f"cases_{status}"]

            status_data_frames.append(data_frame[columns_to_use])

        country_detailed_df = reduce(
            lambda left, right: pd.merge(left, right, on="province", how="left"),
            status_data_frames,
        )

        countries_data_frames.append(country_detailed_df)

    return pd.concat(countries_data_frames)


def remove_unnecessary_countries(data_frame):
    return data_frame[
        ~data_frame["country"].isin(
            [
                *map(lambda x: x.capitalize(), DETAILED_COUNTRIES),
                "United States",
                "Antarctica",
            ]
        )
    ]


def get_geospatial_data():
    detailed_countries_df = gpd.read_file(BackendSettings.DETAILED_COUNTRIES_FILE_PATH)
    world_df = gpd.read_file(BackendSettings.WORLD_FILE_PATH)
    world_df.columns = ["country", "gmi_cntry", "region", "geometry"]
    world_df["province"] = ""
    columns = ["country", "province", "geometry"]

    world_df = remove_unnecessary_countries(world_df)[columns]
    detailed_countries_df = detailed_countries_df[columns]

    return world_df, detailed_countries_df


def scale_colors(values):
    mean = values.mean()
    standard_deviation = values.std()
    outlier_free_max_value = values[values < mean + 3 * standard_deviation].max()
    color_coeffs = (values / outlier_free_max_value) * 0.9
    return np.minimum(1, color_coeffs)


def calculate_color_coefficient(data_frame, scaling_lookup_field="cases_confirmed"):
    data_frame["color"] = scale_colors(data_frame[scaling_lookup_field])
    return data_frame


def inplace_empty_data(data_frame):
    data_frame["created_at"] = datetime.utcnow()
    data_frame["province"] = data_frame["province"].map(
        lambda x: models.VirusSpreadRecord.NOT_GIVEN if x == "" else x
    )


DB_COLUMNS = [
    "country",
    "province",
    "cases_confirmed",
    "cases_deaths",
    "cases_recovered",
    "created_at",
]
JSON_WRITE_FIELDS = [
    "country",
    "province",
    "cases_confirmed",
    "cases_deaths",
    "cases_recovered",
    "color",
    "geometry",
]

TOTAL_STAT_FIELDS = [
    "cases_confirmed",
    "cases_deaths",
    "cases_recovered",
    "cases_confirmed_new",
    "cases_deaths_new",
    "cases_recovered_new",
]


def update_total_data():
    cases_for_all_countries = COVID19API.get_world_total_cases()
    data_frame = serializers.WorldDataTotalAndNewSerializer.serialize_json_list(
        cases_for_all_countries, list_field_name="Countries"
    )
    summarized_daily_stat = (
        data_frame[TOTAL_STAT_FIELDS].apply(np.sum, axis=0).to_dict()
    )

    daily_stat_record = models.VirusDailyStatRecord(**summarized_daily_stat)

    db.session.add(daily_stat_record)
    db.session.commit()


def update_data():
    world_by_countries_cases = extract_world_data()
    detailed_countries_cases = extract_detailed_countries_data()

    world_geo, detailed_geo = get_geospatial_data()
    world_geo_data = pd.merge(world_geo, world_by_countries_cases, how="left")
    detailed_geo_data = pd.merge(detailed_geo, detailed_countries_cases, how="left")

    total = pd.concat([world_geo_data, detailed_geo_data], ignore_index=True)
    total = total.drop_duplicates(["country", "province"], keep="last")

    calculate_color_coefficient(total)
    inplace_empty_data(total)

    total[DB_COLUMNS].to_sql(
        name=models.VirusSpreadRecord.__table_name__,
        con=db.engine,
        index=False,
        if_exists="append",
    )

    with open(f"{BackendSettings.STATIC_DIR}/corona_spread.geojson", "w") as f:
        f.write(total[JSON_WRITE_FIELDS].to_json())

    logging.warning(
        f"Virus spread data is updated in database and geojson file"
        f" {datetime.now().strftime('%Y-%m-%d %H:%M:%SZ')}"
    )
