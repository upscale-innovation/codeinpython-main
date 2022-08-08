from rest_framework.exceptions import APIException


class APIException400(APIException):
    status_code = 400
