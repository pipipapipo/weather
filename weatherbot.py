import requests
from twilio.rest import Client

# Twilio credentials (from Twilio Console)
account_sid = 'ACfc2021d3176e7c83054f57aebdf0304e'
auth_token = 'fe0f6b812f6c54dfbdc5a4799a1a1959'
from_whatsapp_number = 'whatsapp:+19787552334'  # Twilio sandbox number

# List of recipient WhatsApp numbers (must have joined sandbox)
recipients = [
    'whatsapp:+6581007753',  # your number
    'whatsapp:+65yyyyyyyy',  # another user
    # Add more as needed
]

# Fetch rainfall data from data.gov.sg
def get_rainfall_data():
    url = 'https://api.data.gov.sg/v1/environment/rainfall'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', [])
        if items:
            readings = items[0].get('readings', [])
            timestamp = items[0].get('timestamp')
            return f"🌧 Rainfall Update @ {timestamp}:\n" + "\n".join(
                f"{r['station_id']}: {r['value']} mm" for r in readings
            )
    return "⚠️ No rainfall data available."

# Send WhatsApp message to all recipients
def send_weather_updates():
    client = Client(account_sid, auth_token)
    weather_info = get_rainfall_data()

    for recipient in recipients:
        message = client.messages.create(
            body=weather_info,
            from_=from_whatsapp_number,
            to=recipient
        )
        print(f"Sent to {recipient}: {message.sid}")

# Run it
if __name__ == "__main__":
    send_weather_updates()
