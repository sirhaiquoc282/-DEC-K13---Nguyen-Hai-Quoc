import aiohttp
import asyncio
import pandas as pd
import os
import re
import ujson as json


url = "https://api.tiki.vn/product-detail/api/v1/products/{}"
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.7",
    "Origin": "https://tiki.vn",
    "Priority": "u=1, i",
    "Referer": "https://tiki.vn/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "X-Guest-Token": "",
}
products_id_file_path = "./products-0-200000(in).csv"
output_dir = "./Pre_processed_data/"

SEMAPHORE_LIMIT = 30
ERROR_APIS_FILE = "error_apis.txt"
MAX_RETRIES = 10
semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)
ids = pd.read_csv(products_id_file_path).iloc[:, 0].tolist()


def pre_processing(raw_data) -> dict:
    try:
        id = raw_data["id"]
        name = raw_data.get("name", "N/A")
        url_key = raw_data.get("url_key", "N/A")
        price = raw_data.get("price", 0)
        description = re.sub(r"<[^>]+>|[\n\t\r]", "", raw_data.get("description", ""))
        images_url = []
        for image in raw_data.get("images", "N/A"):
            valid_urls = {
                key: value
                for key, value in image.items()
                if isinstance(value, str) and value.startswith("http")
            }
            images_url.append(valid_urls)
        return {
            "id": id,
            "name": name,
            "url_key": url_key,
            "price": price,
            "description": description,
            "images_url": images_url,
        }
    except KeyError as e:
        print(f"Missing key in data: {e}")
        return None


def error_api(id, status_code):
    with open(ERROR_APIS_FILE, "a", encoding="utf-8") as f:
        f.write(url.format(id) + f" - {status_code}\n")


async def fetch_one(session, id, retries=MAX_RETRIES):
    try:
        for attempt in range(1, retries + 1):
            async with session.get(url.format(id), headers=headers) as resp:
                if resp.status == 200:
                    print(f"ID: {id} - status: 200")
                    return pre_processing(await resp.json())
                elif resp.status == 429:
                    print(f"ID: {id} - status: 429 retrying ...")
                    await asyncio.sleep(2**attempt)
                else:
                    print(f"ID: {id} - status: {resp.status}")
                    error_api(id, resp.status)
        print(f"ID: {id} Failed retrying")
        error_api(id, 429)
        return None
    except Exception as e:
        print("ID: {id} - Error: {e}")
        error_api(id, resp.status)
        return None


async def semaphore_control(semaphore, session, id):
    async with semaphore:
        return await fetch_one(session, id)


async def fetch_all(ids):
    async with aiohttp.ClientSession() as session:
        tasks = [semaphore_control(semaphore, session, id) for id in ids]
        responses = await asyncio.gather(*tasks)
        return [resp for resp in responses if resp is not None]


def split_json(json_file, output_dir, chunk_size=1000):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    record_number = 0
    chunk = []
    for i, data in enumerate(json_file):
        chunk.append(data)
        if len(chunk) >= chunk_size:
            output_file = os.path.join(output_dir, f"products{record_number}-{i}.json")
            with open(output_file, "a", encoding="utf-8") as f:
                json.dump(chunk, f, indent=4, ensure_ascii=False)
            record_number = i + 1
            chunk = []
    if chunk:
        output_file = os.path.join(
            output_dir, f"products{record_number}-{len(json_file)}.json"
        )
        with open(output_file, "a", encoding="utf-8") as f:
            json.dump(chunk, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    data = asyncio.run(fetch_all(ids))
    split_json(data, output_dir, chunk_size=1000)

