import requests
import httpx
import asyncio

from utils import data_logger


class Request:
    """
    docstring
    """

    def __init__(self, url_dict: dict):
        self.url_dict = url_dict
        self.logger = data_logger.Logger().set_logger(__name__)

    def sync_request(self, url):
        try:
            with requests.Session() as session:
                request = session.get(url)
                request.raise_for_status()
                return request.content

        except requests.exceptions.HTTPError as http_error:
            self.logger.error(f"Http Error: {http_error}")

        except requests.exceptions.ConnectionError as connection_error:
            self.logger.error(f"Error Connecting:{connection_error}")

        except requests.exceptions.Timeout as timeout_error:
            self.logger.error(f"Timeout Error:{timeout_error}")

        except requests.exceptions.RequestException as general_error:
            self.logger.error(f"Ops Something Else: {general_error}")

    async def async_request(self, url):
        try:
            async with httpx.AsyncClient() as session:
                request = await session.get(url)
                request.raise_for_status()
                return request.content

        except httpx.ConnectError as connection_error:
            self.logger.error(f"Error Connecting:{connection_error}")
            raise connection_error

        except httpx.TimeoutException as timeout_error:
            self.logger.error(f"Timeout Error:{timeout_error}")
            raise timeout_error

        except httpx.RequestError as request_error:
            self.logger.error(f"Request erros: {request_error}")
            raise request_error

        except httpx.HTTPError as http_error:
            self.logger.error(f"Http Error: {http_error}")
            raise http_error

        except RuntimeError as warning:
            self.logger.warning(f"Warning: {warning}")
            pass

        except Exception as general_error:
            self.logger.error(f"Ops Something Else: {general_error}")
            raise general_error

    async def get_data(self, method='a'):
        try:
            if (isinstance(method, str) and method == 'a'):
                task_list = []
                for key, value in self.url_dict.items():
                    result = self.url_dict[key] = self.async_request(value)
                    task_list.append(result)

                await asyncio.gather(*task_list)

            elif (isinstance(method, str) and method == 's'):
                for key, value in self.url_dict.items():
                    result = self.url_dict[key] = self.sync_request(value)

                return result

        except Exception as error:
            self.logger.error(f'Error: {error}')
            raise error
