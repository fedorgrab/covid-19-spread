import json

import pandas as pd


class PandasDataFrameDeserializer:
    """
    Base class implementing deserialization of data from API to Pandas DataFrames.

    Inheriting from this class it is required to:
        Override attribute ``field_mapping``
        OR
        Override class method ``get_field_mapping()``

    You may want to use ``get_field_mapping()`` when field mapping names are dynamically
    calculated.

    The purpose of inheritors of the class is to simply provide how different objects from
    different APIs should be transformed in a consistent data frame.

    """

    field_mapping = None

    # Values which in our data frame should be different from API
    # It is mapped by our side fields names
    # Should be presented as dict of dicts
    api_values_change_on = None

    @classmethod
    def get_field_mapping(cls):
        raise NotImplementedError(
            f"{cls.__class__.__name__} should include either "
            f"`field_mapping` attribute or overridden `get_field_mapping` method"
        )

    @classmethod
    def map_api_values_to_our_format(cls, json_obj, our_field_name, their_field_name):
        their_our_value_mapping = None

        try:
            their_value = json_obj[their_field_name]
        except KeyError:
            raise ValueError(
                f"Provided JSON object does not contain field `{their_field_name}`"
            )

        if cls.api_values_change_on is not None:
            their_our_value_mapping = cls.api_values_change_on.get(our_field_name)

        if (
            their_our_value_mapping is not None
            and their_value in their_our_value_mapping
        ):
            return their_our_value_mapping[their_value]

        return their_value

    @classmethod
    def serialize_object(cls, json_obj):
        pandas_row_obj = {}
        field_mapping = cls.field_mapping or cls.get_field_mapping()

        for pandas_column_name, json_field_name in field_mapping.items():
            value = cls.map_api_values_to_our_format(
                json_obj=json_obj,
                our_field_name=pandas_column_name,
                their_field_name=json_field_name,
            )
            pandas_row_obj[pandas_column_name] = value

        return pandas_row_obj

    @classmethod
    def deserialize_json_list(cls, json_data_raw, list_field_name=None):
        json_data = json.loads(json_data_raw)
        json_list = json_data[list_field_name] if list_field_name else json_data

        field_mapping = cls.field_mapping or cls.get_field_mapping()
        data_frame = pd.DataFrame(columns=field_mapping.keys())

        for json_obj in json_list:
            pandas_instance_dict = cls.serialize_object(json_obj=json_obj)
            data_frame = data_frame.append(pandas_instance_dict, ignore_index=True)

        return data_frame


class CountrySerializer(PandasDataFrameDeserializer):
    field_mapping = {"slug": "Slug"}


class WorldDataTotalSerializer(PandasDataFrameDeserializer):
    field_mapping = {
        "country": "Country",
        "cases_confirmed": "TotalConfirmed",
        "cases_deaths": "TotalDeaths",
        "cases_recovered": "TotalRecovered",
    }
    api_values_change_on = {
        "country": {
            "Russian Federation": "Russia",
            "Iran, Islamic Republic of": "Iran",
            "Belarus": "Byelarus",
        }
    }


class WorldDataTotalAndNewSerializer(PandasDataFrameDeserializer):
    field_mapping = {
        "country": "Country",
        "cases_confirmed": "TotalConfirmed",
        "cases_deaths": "TotalDeaths",
        "cases_recovered": "TotalRecovered",
        "cases_confirmed_new": "NewConfirmed",
        "cases_deaths_new": "NewDeaths",
        "cases_recovered_new": "NewRecovered",
        "date": "Date",
    }
    api_values_change_on = {
        "country": {
            "Russian Federation": "Russia",
            "Iran, Islamic Republic of": "Iran",
            "Belarus": "Byelarus",
        }
    }


class CountryDetailStatusSerializer(PandasDataFrameDeserializer):
    CASE_STATUS = None
    api_values_change_on = {
        "country": {"United States of America": "US"},
        "province": {"Quebec": "Québec"},
    }

    @classmethod
    def get_field_mapping(cls):
        return {
            "country": "Country",
            "province": "Province",
            "lat": "Lon",
            "long": "Lat",
            f"cases_{cls.CASE_STATUS}": f"{cls.CASE_STATUS.capitalize()}",
        }


class CountryDetailConfirmed(CountryDetailStatusSerializer):
    CASE_STATUS = "confirmed"


class CountryDetailDeaths(CountryDetailStatusSerializer):
    CASE_STATUS = "deaths"


class CountryDetailRecovered(CountryDetailStatusSerializer):
    CASE_STATUS = "recovered"


class DayOneByCountrySerializer(PandasDataFrameDeserializer):
    CASE_STATUS = None
    api_values_change_on = {
        "country": {
            "United States of America": "US",
            "Russian Federation": "Russia",
            "Iran, Islamic Republic of": "Iran",
            "Belarus": "Byelarus",
        }
    }

    @classmethod
    def get_field_mapping(cls):
        return {
            "country": "Country",
            "date": "Date",
            f"cases_{cls.CASE_STATUS}": f"Cases",
        }


class DayOneByCountryConfirmed(DayOneByCountrySerializer):
    CASE_STATUS = "confirmed"


class DayOneByCountryDeaths(DayOneByCountrySerializer):
    CASE_STATUS = "deaths"


class DayOneByCountryRecovered(DayOneByCountrySerializer):
    CASE_STATUS = "recovered"


SERIALIZER_STATUS_MAPPING = {
    "confirmed": CountryDetailConfirmed,
    "deaths": CountryDetailDeaths,
    "recovered": CountryDetailRecovered,
}

DAY_ONE_SERIALIZER_STATUS_MAPPING = {
    "confirmed": DayOneByCountryConfirmed,
    "deaths": DayOneByCountryDeaths,
    "recovered": DayOneByCountryRecovered,
}
