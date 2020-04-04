import pandas as pd


class PandasDataFrameSerializer:
    field_mapping = None

    @classmethod
    def get_field_mapping(cls):
        raise NotImplementedError(
            f"{cls.__class__.__name__} should include either "
            f"`field_mapping` attribute or overridden `get_field_mapping` method"
        )

    @classmethod
    def serialize_object(cls, json_obj):
        pandas_row_obj = {}
        field_mapping = cls.field_mapping or cls.get_field_mapping()

        for pandas_column_name, json_field_name in field_mapping.items():
            try:
                pandas_row_obj[pandas_column_name] = json_obj[json_field_name]
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


class WorldDataTotalAndNewSerializer(PandasDataFrameSerializer):
    field_mapping = {
        "country": "Country",
        "cases_confirmed": "TotalConfirmed",
        "cases_deaths": "TotalDeaths",
        "cases_recovered": "TotalRecovered",
        "cases_confirmed_new": "NewConfirmed",
        "cases_deaths_new": "NewDeaths",
        "cases_recovered_new": "NewRecovered"
    }


class CountryDetailStatusSerializer(PandasDataFrameSerializer):
    CASE_STATUS = None

    @classmethod
    def get_field_mapping(cls):
        return {
            "country": "Country",
            "province": "Province",
            "lat": "Lon",
            "long": "Lat",
            f"cases_{cls.CASE_STATUS}": "Cases",
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
    "recovered": CountryDetailRecovered
}
