__all__ = [
    'CheckServiceSession',
    'IMEIChecker',
]

from typing import Dict

from requests import Session, Response


class CheckServiceSession(Session):

    def __init__(self, base_url: str):
        super(CheckServiceSession, self).__init__()

        self.base_url = base_url

    def request(self, method: str, url: str, **kwargs) -> Response:
        return super(CheckServiceSession, self).request(method, self.base_url, **kwargs)

    def check_imei(self, data: Dict, **kwargs) -> Response:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        kwargs.setdefault('headers', headers)
        return self.post(url=self.base_url, data=data, **kwargs)


class IMEIChecker:
    service_url = 'https://api.ifreeicloud.co.uk'

    def __init__(self, service: str, api_key: str):
        self.session = CheckServiceSession(base_url=self.service_url)
        self.service = service
        self.api_key = api_key

    def check_imei(self, imei: str) -> Response:
        data = {
            'service': self.service,
            'key': self.api_key,
            'imei': imei,
        }
        response = self.session.check_imei(
            data=data,
        )
        response.raise_for_status()
        return response.json()
