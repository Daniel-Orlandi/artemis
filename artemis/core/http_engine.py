import requests
import httpx
import asyncio

import jxmlease
from utils import data_logger
from artemis.core import response_handler


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
    """

    def __init__(self, data_dict: dict) -> None:        
        self.data_dict = data_dict
        self.logger = data_logger.Logger().set_logger(__name__)

    def get_data(self):
        return self.data_dict        

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
                self.data_dict[key] = response.content.json()
                return response.status_code

        except AttributeError as atrb_error:
            self.data_dict[key] = response_handler.xml_response(
                response.content)
            self.logger.warning(
                f"Warning: {atrb_error}, returning response as xml")
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
                self.data_dict[key] = response.content.json()
                return response.status_code

        except AttributeError as atrb_error:
            self.data_dict[key] = response_handler.xml_response(
                response.content)
            self.logger.warning(
                f"Warning: {atrb_error}, returning response as xml")
            return response.status_code

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

    async def data(self, method: str = 'a'):
        """
         Orchestrator for running either of the request method.
         Used chained coroutine architecture for compatbility with asyncio

        Parameters
        ----------
        method: str
            a for asynchronous execution, s for synchronous execution.
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
            if (isinstance(method, str) and method == 'a'):
                self.logger.info("async mode selected.")                
                task_list = []
                for id_locale, url in self.data_dict.items():                    
                    result = self.async_request(id_locale, url)
                    task_list.append(result)

                await asyncio.gather(*task_list)

            elif (isinstance(method, str) and method == 's'):
                self.logger.info("sync mode selected.")
                for id_locale, url in self.data_dict.items():
                    self.sync_request(id_locale, url)

        except asyncio.CancelledError as error:
            self.logger.error(f'Error: {error}')
            raise error

        except Exception as error:
            self.logger.error(f'Error: {error}')
            raise error
