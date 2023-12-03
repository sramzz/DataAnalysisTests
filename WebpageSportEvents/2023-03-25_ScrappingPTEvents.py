import requests
import json
import csv

def export_fixtures_to_csv(country: str, start_date: str, end_date: str) -> None:
    """
    Fetches fixture data from the Fixture Calendar API for the given country and date range,
    saves the data to a JSON file and exports the relevant data to a CSV file. 
    The range is limited to 15 days max.

    Args:
        country (str): The name of the country for which to fetch fixture data.
        start_date (str): The start date of the date range in DD/MM/YYYY format.
        end_date (str): The end date of the date range in DD/MM/YYYY format.

    Returns:
        None.
    """
    #formatted for saving the files
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


    if response.status_code == 200:
        allfixtures = response.json()
        with open('fixtures.json', 'w') as f:
            json.dump(allfixtures, f)
        print("Data saved to fixtures.json")

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

        filename = f'events{country}{start_date_formatted}_{end_date_formatted}.csv'

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write the header row
            writer.writerow(dict_event.keys())

            # Write the data rows
            for row in zip(*dict_event.values()):
                writer.writerow(row)

        print(f'Data exported to {filename}')
    else:
        print("Failed to get data. Error code:", response.status_code)



