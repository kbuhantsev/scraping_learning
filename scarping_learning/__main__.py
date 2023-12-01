from datetime import datetime
import logging
import sys
from concurrent.futures import ThreadPoolExecutor

import aiohttp

from scarping_learning.connect_mongo import get_connection
from scarping_learning.models import City, Section, Notice
from scarping_learning.parcer import get_page_soup, handle_notices
import asyncio


db = get_connection()
if db is None:
    raise Exception("no connection to mongo db!")


async def start():
    sections = Section.objects()

    loop = asyncio.get_running_loop()

    for section in sections:
        with ThreadPoolExecutor(4) as pool:
            soups = []
            for city in City.objects:
                soups.append(
                    loop.run_in_executor(
                        pool, get_page_soup, city.city_id, section.section_id
                    )
                )

            result = await asyncio.gather(*soups, return_exceptions=True)

        for idx, soup in enumerate(result):
            handle_notices(soup, City.objects[idx].city_id, section)

        break


async def main():
    # await save_cities()
    await save_notices()


async def save_cities() -> None:
    async with aiohttp.ClientSession("https://market.lun.ua") as session:
        async with session.get("/api/navigation/top-geo") as resp:
            cities_data = await resp.json()
            for city in cities_data["premium"]:
                label = city["label"]
                value = city["value"]
                City.objects(city_id=value).update_one(
                    city_name=label, city_id=value, upsert=True
                )


async def save_notices() -> None:
    params = {
        "geo_id": 0,
        "group_collapse": 1,
        "is_without_fee": "false",
        "lang": "uk",
        "section_id": 0,
        "sort": "insert_time",
        "without_broker": "owner",
    }

    async with aiohttp.ClientSession("https://market.lun.ua") as session:
        for section in Section.objects():
            params["section_id"] = section.section_id
            for city in City.objects():
                params["geo_id"] = city.city_id
                async with session.get("/api/realties", params=params) as resp:
                    notices_data = await resp.json()
                    for notice in notices_data["data"]:
                        if not len(Notice.objects(notice_id=notice["id"])):
                            notice_id = notice["id"]
                            Notice(
                                city_id=city.city_id,
                                section_id=section.section_id,
                                notice_id=notice_id,
                                notice_data=notice,
                                notice_url=f"https://market.lun.ua/uk/redirect/{notice_id}",
                                creation_date=datetime.fromisoformat(notice["download_time"]),
                            ).save()
                            logging.info(
                                f"added notice: {section.section_title} {notice_id} {city.city_name} {notice['geo']}"
                            )


if __name__ == "__main__":
    logging.basicConfig(
        format="%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s",
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(stream=sys.stdout),
            # logging.FileHandler(filename=path_to_file, mode="a")
        ],
        encoding="utf-8",
    )

    # asyncio.run(start())
    asyncio.run(main())
