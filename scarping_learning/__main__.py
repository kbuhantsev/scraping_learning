import logging
import sys
from concurrent.futures import ThreadPoolExecutor

from scarping_learning.models import City, Section
from scarping_learning.parcer import get_page_soup, handle_notices
import asyncio


async def start():

    sections = Section.objects()

    loop = asyncio.get_running_loop()

    for section in sections:

        with ThreadPoolExecutor(3) as pool:

            soups = []
            for city in City.objects:
                soups.append(loop.run_in_executor(pool, get_page_soup, city.city_id, section.section_id))

            result = await asyncio.gather(*soups, return_exceptions=True)

        for idx, soup in enumerate(result):
            handle_notices(soup, City.objects[idx].city_id)

        break


if __name__ == "__main__":
    logging.basicConfig(
        format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(stream=sys.stdout),
            # logging.FileHandler(filename=path_to_file, mode="a")
        ],
    )

    asyncio.run(start())
