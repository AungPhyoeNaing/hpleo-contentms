import httpx
import asyncio

async def check_url(url):
    print(f"Testing: {url}")
    params = {"ac": "videolist", "pg": 1}
    async with httpx.AsyncClient(verify=False) as client:
        try:
            resp = await client.get(url, params=params, timeout=10)
            print(f"Status: {resp.status_code}")
            print(f"Content-Type: {resp.headers.get('content-type')}")
            try:
                data = resp.json()
                print("JSON Decode: Success")
                print(f"Keys: {list(data.keys())}")
            except:
                print(f"JSON Decode: Failed. First 100 chars: {resp.text[:100]}")
        except Exception as e:
            print(f"Error: {e}")
    print("-" * 20)

async def main():
    urls = [
        "https://api.caobizy.com/api.php/provide/vod/",
        "https://www.caobizy.com/api.php/provide/vod/",
        "http://www.caobizy.com/api.php/provide/vod/",
    ]
    for url in urls:
        await check_url(url)

if __name__ == "__main__":
    asyncio.run(main())
