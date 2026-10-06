# myOwn weather app build from scratch

import sys
import requests

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt


class UcheWeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather = QPushButton("Get Weather", self)
        self.temp_label = QLabel(self)
        self.label_emoji = QLabel(self)
        self.label_descript = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Uche Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.label_emoji)
        vbox.addWidget(self.label_descript)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.label_emoji.setAlignment(Qt.AlignCenter)
        self.label_descript.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather.setObjectName("get_weather")
        self.temp_label.setObjectName("temp_label")
        self.label_emoji.setObjectName("label_emoji")
        self.label_descript.setObjectName("label_descript")

        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: Calibri;
            }

            QLabel#city_label {
                font-size: 40px;
                font-weight: bold;
                font-style: italic;
            }

            QLineEdit#city_input {
                font-size: 40px;
            }

            QPushButton#get_weather {
                font-size: 30px;
                font-weight: bold;
            }

            QLabel#temp_label {
                font-size: 40px;
            }

            QLabel#label_descript {
                font-size: 75px;
            }

            QLabel#label_emoji {
                font-size: 100px;
                font-family: "Segoe UI Emoji";
            }
        """)

        self.get_weather.clicked.connect(self.get_weather_button)

    def get_weather_button(self):
        api_key = "a65a9e40fd60aada4c63d4146372e3e4"
        city = self.city_input.text().strip()

       

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data.get("cod") == 200:
                self.display_weather(data)
            else:
                self.display_error(data.get("message", "City not found."))

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                     self.display_error("bad request:\nplease check your input")
                case 401:
                      self.display_error("Unauthourized:\nInvid API key")
                case 403:
                      self.display_error("Forbidden:\nAccess denied")
                case 404:
                      self.display_error("Not found:\ncity not found")
                case 500:
                      self.display_error("Internal Server Error:\nplease try again")
                case 502:
                      self.display_error("Bad Gateway:\ninvalid response from server")
                case 503:
                      self.display_error("Service unavailable:\nserver is down")
                case 504:
                      self.display_error("Gateway timeout:\nNo response from the server")
                case _:
                      self.display_error(f"http error occured:\n{http_error}")
                
                
     
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
                    self.display_error("Timed Error:\nThe Request is timed out")
        except requests.exceptions.TooManyRedirects:
                    self.display_error("Too many Redirects:\nCheck your internet connection")
        except requests.exceptions.RequestException as req_error:
                    self.display_error(f"Request Error:\n{req_error}")  

    def display_error(self, message):
        # self.setStyleSheet("QLabel#temp_label { font-size: 30px; }")
        self.temp_label.setText(message)
        self.label_emoji.clear()
        self.label_descript.clear()

    def display_weather(self, data):
        # self.setStyleSheet("QLabel#temp_label { font-size: 75px; }")
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9/5) + 32

        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        self.temp_label.setText(f"{temperature_f:.0f}°F")
        self.label_emoji.setText(self.get_weather_emoji(weather_id))
        self.label_descript.setText(f"{weather_description}")

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"  
        elif 300 <= weather_id <= 321:
            return "🌦️"  
        elif 500 <= weather_id <= 531:
            return "🌧️"  
        elif 600 <= weather_id <= 622:
            return "❄️"  
        elif 701 <= weather_id <= 741:
            return "🌫️"  
        elif weather_id == 762:
            return "🌋"  
        elif weather_id == 771:
            return "💨"  
        elif weather_id == 781:
            return "🌪️"  
        elif weather_id == 800:
            return "☀️"  
        elif 801 <= weather_id <= 804:
            return "☁️"  
        else:
            return "❓"  



if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = UcheWeatherApp()
    weather_app.show()
    sys.exit(app.exec_())


