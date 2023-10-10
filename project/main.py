from project.temp_convert import CelsiusToFahrenheit, FahrenheitToCelsius

if __name__ == '__main__':
    conv = CelsiusToFahrenheit()
    print(
        conv.parse(
            conv.convert('20')
        )
    )
