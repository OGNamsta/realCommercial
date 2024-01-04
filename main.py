import httpx
import asyncio
import json
import os
import pandas as pd


# headers = {
#     'Accept': '*/*',
#     'Accept-Language': 'en-US,en;q=0.9,en-GB;q=0.8,de;q=0.7,es;q=0.6',
#     'Cache-Control': 'no-cache',
#     'Connection': 'keep-alive',
#     'Content-Type': 'application/json',
#     'DNT': '1',
#     'Origin': 'https://www.realcommercial.com.au',
#     'Pragma': 'no-cache',
#     'Referer': 'https://www.realcommercial.com.au/',
#     'Sec-Fetch-Dest': 'empty',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Site': 'same-site',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#     'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
# }
#
# page_no = 1
# json_data = {
#     'channel': 'rent',
#     'filters': {
#         'within-radius': 'includesurrounding',
#         'surrounding-suburbs': True,
#     },
#     'page': {page_no},
#     'page-size': 10,
# }
#
# # In-memory cache for storing the response.
# response_cache = {}
#
#
# async def fetch_data():
#     async with httpx.AsyncClient() as client:
#         response = await client.post('https://api.realcommercial.com.au/listing-ui/nearby-searches', headers=headers, json=json_data)
#         return response
#
#
# async def main():
#     # Loop through the pages. Increasing the page number by 1.
#     for page_no in range(1, 10):
#         json_data["page"] = page_no
#         filename = f'{json_data["page"]}.json'
#
#         # Check if the file exists.
#         if os.path.exists(filename):
#             print(f'File {filename} already exists.')
#             continue
#
#         # Check if response is cached.
#         if json_data["page"] in response_cache:
#             print(f'Response for page {json_data["page"]} is cached.')
#             response = response_cache[json_data["page"]]
#         else:
#             # If not in the cache, fetch the data and store it in the cache.
#             print(f'Response for {json_data["page"]} not cached.')
#             response = await fetch_data()
#             response_cache[json_data["page"]] = response
#         # Save response to file. Filename is the page number.
#         with open(f'{json_data["page"]}.json', 'w', encoding='utf-8') as f:
#             f.write(response.text)

# Function to process JSON file and return a dataframe.
def process_json_file(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)

    # Extracting id and highlights for each listing
    data = {'property_id': [], 'highlights': [], 'agencies': []}
    for listing in json_data.get('listings', []):
        property_id = listing.get('id', '')
        highlights = listing.get('highlights', [])

        agencies_data = listing.get('agencies', [])
        agencies = []

        # Print the number of agencies for each listing
        print(len(f'Agencies for property {property_id}: {agencies_data}'))

        for agency_data in agencies_data:
            agency_id = agency_data.get('id', '')
            agency_name = agency_data.get('name', '')

            salespeople_data = agency_data.get('salespeople', [])
            salespeople = []

            for salesperson_data in salespeople_data:
                salesperson_id = salesperson_data.get('id', '')
                salesperson_name = salesperson_data.get('name', '')
                salesperson_image_path = salesperson_data.get('imagePath', '')
                salesperson_image_url_template = salesperson_data.get('imageUrlTemplate', '')

                salespeople.append({
                    'salesperson_id': salesperson_id,
                    'salesperson_name': salesperson_name,
                    'salesperson_image_path': salesperson_image_path,
                    'salesperson_image_url_template': salesperson_image_url_template,
                })

            agencies.append({
                'agency_id': agency_id,
                'agency_name': agency_name,
                'salespeople': salespeople,
            })

        data['property_id'].append(property_id)
        data['highlights'].append(', '.join(highlights) if highlights else '')
        data['agencies'].append(agencies)

    # Creating a DataFrame
    df = pd.DataFrame(data)

    # Exploding nested columns for agencies
    df_expanded = df.explode('agencies')
    df_expanded = pd.concat([df_expanded.drop(['agencies'], axis=1), df_expanded['agencies'].apply(pd.Series)], axis=1)

    # Exploding nested columns for salespeople
    df_expanded = df_expanded.explode('salespeople')
    df_expanded = pd.concat([df_expanded.drop(['salespeople'], axis=1), df_expanded['salespeople'].apply(pd.Series)], axis=1)

    # Return the dataframe
    return df_expanded


# Folder containing the JSON files.
json_folder = 'C://Users//tenge//dev//Python//Data Scraping//realCommercial//jsonFiles'

# List to store the dataframes for each file
dfs = []

# Choose a specific file to process.
file_path = os.path.join(json_folder, '1Test.json')
file_path = os.path.abspath(file_path)

# Process the file and append the dataframe to the list.
df = process_json_file(file_path)

# Save the dataframe to a CSV file.
df.to_csv('excelFiles/1Test1.csv', index=False)

# Print the dataframe.
print(df)