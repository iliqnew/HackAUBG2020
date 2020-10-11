import requests
from bs4 import BeautifulSoup
import threading
import json

#fahrenheit to celcius T(C) = (T(F) - 32) * 5/9


class Classifier:
    def __init__(self):
        self.countries_url = "https://www.climatestotravel.com/world-climates/countries"
        self.session = None
        self.soup = None

        self.countries = []

    def getPage(self, url):
        self.session = requests.Session()
        page = self.session.get(url)
        self.soup = BeautifulSoup(page.content, "html.parser")
    
    def getCountries(self):
        self.getPage(self.countries_url)
        return [Country(a.text[1:]) for a in self.soup.find("div", class_="ElencoPaesi").find_all("a") if a["href"].count("/") == 2]
    
    def main(self):
        self.countries = self.getCountries()
        for country in self.countries:
            try:
                x = threading.Thread(target=country.main, args=())
                x.start()
            except Exception as e:
                print(e)
                del(country)



class Country(Classifier):
    def __init__(self, name):
        self.name = name
        self.capital = ""
        self.country_code = ""
        
        self.climate_url = "https://www.climatestotravel.com" + "/climate/" + self.name

        self.climate = {}
        self.wind = 0
        self.temperature = 0
        self.temp_departure = 0
        self.humidity = 0
        self.palmer_draught = 0
        self.days_since_recipit = 0

        self.risk = 0

    def getClimate(self):
        
        self.getPage(self.climate_url)
        
        avg_temperature = self.soup.find("table", class_="cities")
        avg_precipitation = self.soup.find("table", class_="precipit")
        sunshine = self.soup.find("table", class_="sole")

        months = [a.text for a in avg_temperature.find("tr", class_="title-table-new").find_all("th") if not a.text == "Month"]
        
        avg_temperature = dict(zip(months, list(zip([int(a.text) for a in avg_temperature.find_all("tr", class_="min-table")[1].find_all("td")], [int(a.text) for a in avg_temperature.find_all("tr", class_="max-table")[1].find_all("td")]))))
        avg_precipitation = dict(zip(months, list(zip([int(a.text) for a in avg_precipitation.find_all("tr", class_="precipit-table")[1].find_all("td")[:-1]], [int(a.text) for a in avg_precipitation.find_all("tr", class_="precipit-table")[2].find_all("td")[:-1]]))))
        sunshine = dict(zip(months, [int(a.text) for a in sunshine.find("tr", class_="sole-table").find_all("td")]))
        
        climate = {"Average Temperature" : avg_temperature,
                    "Average Precipitation" : avg_precipitation,
                    "Sunshine" : sunshine}
        print(self.name + ": " + str(climate))
        return climate
            
            
    
    def getWind(self):
        self.getPage(self.climate_url)
        return 0

    def getTemperature(self):
        self.getPage(self.climate_url)
        return 0

    def getTempDeparture(self):
        self.getPage(self.climate_url)
        return 0

    def getHumidity(self):
        self.getPage(self.climate_url)
        return 0
    
    def getPalmerDraught(self):
        self.getPage(self.climate_url)
        return 0
    
    def getDaysSinceRecipit(self):
        self.getPage(self.climate_url)
        return 0
    
    def riskAssessment(self):
        self.climate = self.getClimate()

        self.wind = self.getWind()
        self.temperature = self.getTemperature()
        self.temp_departure = self.getTempDeparture()
        self.humidity = self.getHumidity()
        self.palmer_draught = self.getPalmerDraught()
        self.days_since_recipit = self.getDaysSinceRecipit()

        self.risk = self.wind * self.temperature * self.days_since_recipit / self.humidity
        #print("Risk for " + self.name + ": " + str(self.risk))
    
    def main(self):
        t = 0
        while t < 3:
            try:
                with open("countries.json", "r") as countries:
                    for country in countries:
                        if country["Country"] == self.name:
                            self.capital = country["Capital"]
                            self.country_code = country["Country Code"]
                            break
                
                self.riskAssessment()
            except Exception as e:
                print(e)
                t += 1
 
if __name__ == "__main__":
    c = Classifier()
    c.main()