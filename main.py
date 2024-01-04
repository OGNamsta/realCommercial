import httpx
import asyncio
import json


headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9,en-GB;q=0.8,de;q=0.7,es;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'DNT': '1',
    'Origin': 'https://www.realcommercial.com.au',
    'Pragma': 'no-cache',
    'Referer': 'https://www.realcommercial.com.au/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

json_data = {
    'channel': 'rent',
    'filters': {
        'within-radius': 'includesurrounding',
        'surrounding-suburbs': True,
    },
    'page': 1,
    'page-size': 10,
}

# In-memory cache for storing the response.
response_cache = {}


async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.post('https://api.realcommercial.com.au/listing-ui/nearby-searches', headers=headers, json=json_data)
        return response


async def main():
    response = await fetch_data()
    # Check if response is cached.
    if json_data["page"] in response_cache:
        print('Response is cached.')
        response = response_cache[json_data["page"]]
    else:
        # If not in the cache, fetch the data and store it in the cache.
        print('Response is not cached.')
        response = await fetch_data()
        response_cache[json_data["page"]] = response
    # Save response to file. Filename is the page number.
    with open(f'{json_data["page"]}.json', 'w', encoding='utf-8') as f:
        f.write(response.text)


if __name__ == '__main__':
    asyncio.run(main())
