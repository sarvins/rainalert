import requests
import os
from twilio.rest import Client
from dotenv import load_dotenv


weather_url:str = "https://api.openweathermap.org/data/2.5/forecast"

load_dotenv()

weather_api_key = os.environ.get("WEATHER_API_KEY")

params = {
  'lat':37.477421,
  'lon':-86.294144, 
  'appid':weather_api_key,
  'cnt':4
}

response = requests.get(url=weather_url, params=params)
response.raise_for_status()
weather_data = response.json()
print(weather_data)


# create id's for the day
def check_weather() -> bool:
  will_rain = False
  for hour_data in weather_data['list']:
    condition_code = hour_data['weather'][0]['id']
    if int(condition_code) < 700:
      will_rain = True
  return will_rain

def send_sms():
  will_rain = check_weather()
  account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
  auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
  number_send = os.environ.get("MOBILE_NUMBER_SEND")
  number_receive = os.environ.get("MOBILE_NUMBER_RECEIVE")
  client = Client(account_sid, auth_token)
  
  if will_rain:
    message = client.messages.create(
      body="It will rain today! take an umbrella!",
      from_=number_send,
      to=number_receive,
    )
  else:
      message = client.messages.create(
      body="It will not rain today!",
      from_= number_send,
      to=number_receive,
    )
      
  print(f"message was sent: {message.status}")

print(check_weather())
send_sms()
