
import requests
from pycti import OpenCTIApiClient, OpenCTIApiConnector

url_cti='YOUR_OpenCTI_URL'
token_cti='YOUR_OPENCTI_TOKEN'

# API CONNECTOR
opencti_api_client = OpenCTIApiClient(
    url=url_cti,
    token=token_cti,
    ssl_verify=False,
    log_level="debug",
    json_logging=True
)

if opencti_api_client.health_check() is True:
    print("status OK")

# LOAD GEOGRAPHY DATASET
response = requests.get('https://raw.githubusercontent.com/OpenCTI-Platform/datasets/master/data/geography.json')
data = response.json()
print(data)

# PARSES COUNTRIES AND LOAD IN OPENCTI
for country_data in data['objects']:
    if 'country' in country_data.keys():
        try:
            if 'x_opencti_aliases' not in country_data.keys():
                country_data['x_opencti_aliases'] = []

            opencti_api_client.location.create(
                name=country_data['name'],
                x_opencti_aliases=country_data['x_opencti_aliases'],
                latitude=country_data['latitude'],
                longitude=country_data['longitude'],
                type=country_data['x_opencti_location_type'],
                country=country_data['country'],
                update=True
            )
        except Exception as e:
            print(e)
            opencti_api_client.location.create(
                name=country_data['name'],
                x_opencti_aliases=country_data['x_opencti_aliases'],
                country=country_data['country'],
                type=country_data['x_opencti_location_type'],
                update=True
            )
