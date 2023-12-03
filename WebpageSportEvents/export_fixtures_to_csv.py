import requests
import json
import csv
from io import StringIO

def export_fixtures_to_csv(country: str, start_date: str, end_date: str) -> str:
    start_date_formatted = start_date.replace('/', '-')
    end_date_formatted = end_date.replace('/', '-')

    url = "https://api.fixturecalendar.com/api/v1/fixtures"

    params = {
        "country": country,
        "startDate": start_date,
        "endDate": end_date
    }

    headers = {
        "accept": "application/json"
    }

    response = requests.get(url, params=params, headers=headers)

    csv_data = None

    if response.status_code == 200:
        allfixtures = response.json()

        dict_event = dict()
        dict_event['date'] = []
        dict_event['name'] = []
        dict_event['location'] = []
        dict_event['sport'] = []
        dict_event['competition'] = []
        for event in allfixtures['events']:
            dict_event['date'].append(event["startTime"])
            dict_event['name'].append(event["cachedFrontEndName"])
            dict_event['location'].append(event['location']['address'])
            dict_event['sport'].append(event['sport']['name'])
            dict_event['competition'].append(event['competition']['name'])

        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)

        # Write the header row
        writer.writerow(dict_event.keys())

        # Write the data rows
        for row in zip(*dict_event.values()):
            writer.writerow(row)

        csv_data = csv_buffer.getvalue()
    else:
        print("Failed to get data. Error code:", response.status_code)

    return csv_data
