import requests
from datetime import date

from Secret import Secret

class AccuWeather:
    zip = 0 #user entered zip, int? String?
    city = ""
    primaryPostalCode = "" #the postal code that is returned by accuweather
    locationId = ""

    # TODO: attempt contact of base_uri and confirm service is available
    def __init__(self, zip):
        self.zip = zip

    #TODO: Consider making this automatic
    #TODO: This blindly selects the first search result
    def zip_code_search(self) -> bool:
        #Make GET request
        json = self.make_request("/locations/v1/postalcodes/search", {"q": self.zip})
        json_v1 = json[0] #select first search result

        self.city = json_v1['LocalizedName']
        self.primaryPostalCode = json_v1['PrimaryPostalCode']
        self.locationId = json_v1['Key']

        #print(self.city)
        #print(self.primaryPostalCode)
        #print(self.locationId)

        return True

    def get_forecast(self, days):
        json = self.make_request("/forecasts/v1/daily/5day/" + self.locationId, {})
        forecasts = json['DailyForecasts']

        for i in range(0, days):
            self.print_day_forecast(forecasts[i])

    def print_day_forecast(self, day_obj):
        d = date.fromisoformat(day_obj['Date'].split("T")[0])
        temp_lo = int(day_obj['Temperature']['Minimum']['Value'])
        temp_hi = int(day_obj['Temperature']['Maximum']['Value'])
        forecast_day = day_obj['Day']['IconPhrase']
        forecast_night = day_obj['Night']['IconPhrase']

        print(self.city + " forecast for " + d.strftime("%A, %B %d"))
        print("lo/hi " + str(temp_lo) + "/" + str(temp_hi))
        print("During the day " + forecast_day)
        print("During the night " + forecast_night)

    def make_request(self, endpoint: str, args: dict):
        BASE_URI = "http://dataservice.accuweather.com"
        url = BASE_URI + endpoint

        #add apikey to querystring
        args['apikey'] = Secret.API_KEY_ACCUWEATHER

        #make the actual request
        response = requests.get(url, args)

        # Done if not 200
        if not response.ok:
            return None

        return response.json()
