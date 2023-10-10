from abc import ABC, abstractmethod
import requests
import xml.etree.ElementTree as ET


class TempConvert(ABC):
    """Base abstract conversion class, defines behavior.

    Fields: url: str | options: dict.
    Methods: convert() -> Response | parse() -> str
    """

    def __init__(self):
        self.url: str = 'https://www.w3schools.com/xml/tempconvert.asmx'
        self.options: dict = {
            'Content-Type': 'text/xml; charset=utf-8',
        }

    @abstractmethod
    def convert(self, value: str) -> requests.Response:
        pass

    @abstractmethod
    def parse(self, data: requests.Response) -> str | None:
        root = ET.fromstring(data.text)
        for child in root.iter("*"):
            if child.text is not None:
                return child.text
        return None


class CelsiusToFahrenheit(TempConvert):
    def __init__(self):
        super().__init__()

    def convert(self, value: str) -> requests.Response:
        """Overridden function. Send a request to API with the created envelope, return a response."""

        envelope = f"""
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
          <soap:Body>
            <CelsiusToFahrenheit xmlns="https://www.w3schools.com/xml/">
              <Celsius>{value}</Celsius>
            </CelsiusToFahrenheit>
          </soap:Body>
        </soap:Envelope>
        """
        return requests.post(self.url, data=envelope, headers=self.options)

    def parse(self, data: requests.Response) -> str | None:
        """Overridden function. Forward this method to the TempConvert."""

        return super().parse(data)


class FahrenheitToCelsius(TempConvert):
    def __init__(self):
        super().__init__()

    def convert(self, value: str) -> requests.Response:
        """Overridden function. Send a request to API with the created envelope, return a response."""
        envelope = f"""
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
          <soap:Body>
            <FahrenheitToCelsius xmlns="https://www.w3schools.com/xml/">
              <Fahrenheit>{value}</Fahrenheit>
            </FahrenheitToCelsius>
          </soap:Body>
        </soap:Envelope>
        """
        return requests.post(self.url, data=envelope, headers=self.options)

    def parse(self, data: requests.Response) -> str | None:
        """Overridden function. Forward this method to the TempConvert."""
        return super().parse(data)
