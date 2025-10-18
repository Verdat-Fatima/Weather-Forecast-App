import requests
import time
from datetime import datetime, timezone, timedelta
import pycountry


API_key='Place your api key'
base_url='https://api.openweathermap.org/data/2.5/weather?'



def update_time(data):
    city_timezone = timezone(timedelta(seconds=data['timezone']))
    print("\n--- Live Local Time ---")  
    try:
        while True:
            current_time = datetime.now(tz=city_timezone)
            print(f"\rLocal time: {current_time.strftime('%I:%M:%S %p')}", end="", flush=True)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped live time display\n")



def weather(c):

    url=f'{base_url}q={c}&appid={API_key}&units=metric'

    try:
        response=requests.get(url,timeout=5)
    except requests.exceptions.RequestException as e:
        print(f'{e}')
        return
    
    data=response.json()

    if response.status_code==200 :
        
        country_code = data['sys']['country']
        country = pycountry.countries.get(alpha_2=country_code)
        country_name = country.name if country else country_code

        print(f"City : {data['name']}")
        print(f"Country : {country_name}")
        print(f"Temperature :{data['main']['temp']} °C")
        print(f"Feels like : {data['main']['feels_like']} °C")
        print(f"Description : {data['weather'][0]['description'].capitalize()}")
        print(f"Pressure : {data['main']['pressure']} hPa")
        print(f"Humidity : {data['main']['humidity']} %")
        update_time(data)
       
    else:
        error=data.get('message','').lower()
        
        if 'invalid api key' in error:
            print('Error: Invalid API key. Please verify your API key on OpenWeatherMap')
        elif response.status_code==429:
            print('Error : Too many requests. You have exceeded your API limit. Try again later')
        elif response.status_code==401:
            print('Error : Unauthorized access. Please check your API key permissions')
        elif response.status_code==404:
            print('Error: The resource or city was not found')

        else:
            print(f"Unexpected error : {data.get('message','Unknown error from API')} Status code : {response.status_code}")


if __name__ == "__main__":
    while True:
        city = input('\nEnter city (or type "exit" to quit): ').strip()
        if city.lower() == "exit":
            print("Exiting program...")
            break
        weather(city)