import pandas as pd


class PandasDataFrameSerializer:
    field_mapping = None
    # Values which in our data frame should be different from API
    # It is mapped by ourside fields names
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
        their_value = json_obj[their_field_name]
        if cls.api_values_change_on is not None:
            their_our_value_mapping = cls.api_values_change_on.get(our_field_name)

        if their_our_value_mapping is not None and their_value in their_our_value_mapping:
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
                their_field_name=json_field_name
            )
            try:
                pandas_row_obj[pandas_column_name] = value
            except KeyError:
                raise ValueError(
                    f"Provided JSON object does not contain field {json_field_name}"
                )
        return pandas_row_obj

    @classmethod
    def serialize_json_list(cls, json_data, list_field_name=None):
        json_list = json_data[list_field_name] if list_field_name else json_data

        field_mapping = cls.field_mapping or cls.get_field_mapping()
        data_frame = pd.DataFrame(columns=field_mapping.keys())

        for json_obj in json_list:
            pandas_instance_dict = cls.serialize_object(json_obj=json_obj)
            data_frame = data_frame.append(pandas_instance_dict, ignore_index=True)

        return data_frame


class WorldDataTotalSerializer(PandasDataFrameSerializer):
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
        }
    }


class WorldDataTotalAndNewSerializer(PandasDataFrameSerializer):
    field_mapping = {
        "country": "Country",
        "cases_confirmed": "TotalConfirmed",
        "cases_deaths": "TotalDeaths",
        "cases_recovered": "TotalRecovered",
        "cases_confirmed_new": "NewConfirmed",
        "cases_deaths_new": "NewDeaths",
        "cases_recovered_new": "NewRecovered",
    }
    api_values_change_on = {
        "country": {
            "Russian Federation": "Russia",
            "Iran, Islamic Republic of": "Iran",
        }
    }


class CountryDetailStatusSerializer(PandasDataFrameSerializer):
    CASE_STATUS = None
    api_values_change_on = {
        "country": {
            "United States of America": "US",
        },
        "province": {
            "Quebec": "Québec"
        }
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


SERIALIZER_STATUS_MAPPING = {
    "confirmed": CountryDetailConfirmed,
    "deaths": CountryDetailDeaths,
    "recovered": CountryDetailRecovered,
}
