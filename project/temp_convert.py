from abc import ABC, abstractmethod
import requests
import xml.etree.ElementTree as ET
from typing import Any


class TempConvert(ABC):
    """Base abstract conversion class, defines behavior.

    Class fields: conversations: None|dict.
    Class methods: get_conversion() -> Any.
    Fields: url: str, options: dict.
    Methods: convert() -> Response, parse() -> str
    """
    conversions: dict[str, Any] = None

    def __init__(self, unit: str) -> None:
        self.unit: str = unit
        self.url: str = 'https://www.w3schools.com/xml/tempconvert.asmx'
        self.options: dict = {
            'Content-Type': 'text/xml; charset=utf-8',
        }

    @classmethod
    def get_conversion(cls, unit: str) -> Any:
        if cls.conversions is None:
            cls.conversions = {}
            for conversion_class in cls.__subclasses__():
                conversion: TempConvert = conversion_class()
                cls.conversions[conversion.unit] = conversion
        return cls.conversions[unit]

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
    def __init__(self) -> None:
        super().__init__('celsius')

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
    def __init__(self) -> None:
        super().__init__('fahrenheit')

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
