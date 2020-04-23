import logging

import requests

from backend.data_mining import exceptions

logger = logging.getLogger(__name__)

API_ERROR_STATUS_CODE_MAPPING = {
    400: exceptions.ServiceError400,
    500: exceptions.ServiceError500,
}


class BaseAPI:
    BASE_URL = None
    REQUEST_TIMEOUT = 150

    @classmethod
    def _request(
        cls,
        method: str,
        endpoint: str,
        data: dict = None,
        headers: dict = None,
        timeout: int = REQUEST_TIMEOUT,
    ) -> str:
        try:
            response = requests.api.request(
                method,
                f"{cls.BASE_URL}{endpoint}",
                json=data,
                headers=headers,
                timeout=timeout,
            )

        except requests.Timeout:
            raise exceptions.RequestTimeout
        except requests.RequestException:
            raise exceptions.ServerError

        if response.status_code in API_ERROR_STATUS_CODE_MAPPING:
            logger.error(msg="API responded with an error")
            raise API_ERROR_STATUS_CODE_MAPPING[response.status_code](
                data=response.json()
            )

        return response.text


class COVID19API(BaseAPI):
    BASE_URL = "https://api.covid19api.com"

    @classmethod
    def get_countries(cls):
        return cls._request(endpoint="/countries", method="get")

    @classmethod
    def get_world_total_cases(cls):
        return cls._request(endpoint="/summary", method="get")

    @classmethod
    def get_details_for_country(cls, country, status, date_after):
        return cls._request(
            endpoint=f"/live/country/{country}/status/{status}/date/{date_after}",
            method="get",
        )

    @classmethod
    def get_day_one_by_country(cls, country, status):
        return cls._request(
            endpoint=f"/total/dayone/country/{country}/status/{status}", method="get"
        )
