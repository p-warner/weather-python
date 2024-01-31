from AccuWeather import AccuWeather

#Get the ZIP
print("Enter a ZIP code: ")
zip = input()

#TODO: Validate zip

#init API wrapper
accu_weather = AccuWeather(zip)
accu_weather.zip_code_search()
accu_weather.get_forecast(3)

print("Done")
