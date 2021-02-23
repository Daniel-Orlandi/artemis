import requests
import httpx
import asyncio
from urllib.parse import urlparse

from artemis.core import response_handler
from artemis.utils.data_logger import Logger


class Request:
    """ 
    Make a  asynchronous or syncronous request to a specific http url,
    from a dict of one or more keys:values.
    ...

    Attributes
    ---------- 
    data_dict: dict
        A dictionary where the key is a locale_id,
        and the value is the url to where the requisition will be made.

    Methods
    -------
    def get_data(self):
        returns data dictionary

    sync_request(self, key, url: str):
        makes a synchronous request to a url.

    async def async_request(self, key, url: str):
        enables support to asynchronous request to a url.

    async def data(self, method='a'):
        Responsible for orchestrate the requests.

    TODO
    -----
    Implement retry strategy
    """

    def __init__(self, data_dict: dict) -> None:
        self.data_dict = data_dict
        self.logger = Logger(logger_name=__name__).get_logger()

    def get_data_dict(self) -> dict:
        return self.data_dict

    @staticmethod
    def get_host(url) -> str:
        return urlparse(url).hostname

    def sync_request(self, key, url: str) -> requests.Response:
        """
        Parameters
        ----------
        key
         locale id

        url: str
         url to be requested.

        Raises
        ----------
        requests.exceptions.HTTPError

        requests.exceptions.ConnectionError  

        requests.exceptions.Timeout

        requests.exceptions.RequestException

        Returns
        ----------
        requests.Response

        """
        try:
            with requests.Session() as session:
                response = session.get(url)
                response.raise_for_status()
                self.data_dict[key] = {'host': self.get_host(
                    str(response.url)), 'data': response_handler.json_response(response.content.decode())}
                return response.status_code

        except ValueError as not_json_error:
            self.logger.warning(
                f"Warning: {not_json_error}. trying to read response as xml")

            self.data_dict[key] = {'host': self.get_host(
                str(response.url)), 'data': response_handler.xml_response(response.content)}

            self.logger.warning(
                f"Warning: read response as xml")
            
            return response.status_code

        except requests.exceptions.HTTPError as http_error:
            self.logger.error(f"Http Error: {http_error}")

        except requests.exceptions.ConnectionError as connection_error:
            self.logger.error(f"Error Connecting:{connection_error}")

        except requests.exceptions.Timeout as timeout_error:
            self.logger.error(f"Timeout Error:{timeout_error}")

        except requests.exceptions.RequestException as general_error:
            self.logger.error(f"Ops Something Else: {general_error}")

    async def async_request(self, key, url: str) -> httpx.Response:
        """
        Parameters
        ----------
        key
         locale id
        url: str
         url to be requested.

        Raises
        ----------
        httpx.ConnectError

        httpx.TimeoutException

        httpx.RequestError

        httpx.HTTPError

        RuntimeError as warning

        Exception
            catches any other error.

        Returns
        ----------
        httpx.Response

        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                self.data_dict[key] = {'host': self.get_host(
                    str(response.url)), 'data': response_handler.json_response(response.content.decode())}
                return response.status_code

        except ValueError as not_json_error:
            self.logger.warning(f"Warning: {not_json_error}. trying to read response as xml")

            self.data_dict[key] = {'host': self.get_host(
                str(response.url)), 'data': response_handler.xml_response(response.content)}

            self.logger.warning(f"Warning: read response as xml")
            return response.status_code        

        except httpx.ConnectError as connection_error:
            self.logger.error(f"Error Connecting:{connection_error}")
            
        except httpx.TimeoutException as timeout_error:
            self.logger.error(f"Timeout Error:{timeout_error}")
           
        except httpx.RequestError as request_error:
            self.logger.error(f"Request erros: {request_error}")
           
        except httpx.HTTPError as http_error:
            self.logger.error(f"Http Error: {http_error}")
            
        except RuntimeError as warning:
            self.logger.warning(f"Warning: {warning}")
            
        except Exception as general_error:
            self.logger.error(f"Ops Something Else: {general_error}")
            
    async def get(self, method: str = "sync"):
        """
         Orchestrator for running either of the request method.
         Used chained coroutine architecture for compatbility with asyncio

        Parameters
        ----------
        method: str = "sync"
            async for asynchronous execution, sync for synchronous execution.
            default method is sync.

        locale id

        url: str

        url to be requested.

        Raises
        ----------
        asyncio.CancelledError
            check if any of the requests were cancelled.
            (not sure if necessary)       

        Exception
            catches any other error.

        """
        try:
            if (isinstance(method, str) and method == 'async'):
                self.logger.info("async mode selected.")

                task_list = []
                for id_locale, url in self.data_dict.items():
                    result = self.async_request(id_locale, url)
                    task_list.append(result)

                await asyncio.gather(*task_list)
                self.logger.info("Done")

            elif (isinstance(method, str) and method == 'sync'):
                self.logger.info("sync mode selected.")

                for id_locale, url in self.data_dict.items():
                    self.sync_request(id_locale, url)
                    self.logger.info("Done")
            
            else:
                raise AttributeError("Method shoud be either sync or async.")

        except asyncio.CancelledError as cancelled_error:
            self.logger.error(f'Cancelled error: {cancelled_error}')            
            
        except Exception as error:
            self.logger.error(f'Error: {error}')
            
            
