import logging
import requests

class Request:

    def __init__(self, site):
        self.__site = site

    @property
    def site(self):
        return self.__site

    def get_data(self):
        try:
            with requests.Session() as session:
                request = session.get(self.__site)
                request.raise_for_status()

            return request

        except requests.exceptions.HTTPError as http_error:
            logging.error(f"Http Error: {http_error}")

        except requests.exceptions.ConnectionError as connection_error:
            logging.error(f"Error Connecting:{connection_error}")

        except requests.exceptions.Timeout as timeout_error:
            logging.error(f"Timeout Error:{timeout_error}")

        except requests.exceptions.RequestException as general_error:
            logging.error(f"Ops Something Else: {general_error}")
