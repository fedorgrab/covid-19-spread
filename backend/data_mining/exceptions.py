class APIError(Exception):
    def __init__(self, data=None, *args, **kwargs):
        self.data = data
        super().__init__(*args, **kwargs)


class ServiceError400(APIError):
    pass


class ServiceError500(APIError):
    pass


class RequestError(Exception):
    pass


class RequestTimeout(RequestError):
    pass


class ServerError(RequestError):
    pass
