import logging
import sys

from scarping_learning.models import City, Section
from scarping_learning.parcer import get_page_soup, handle_notices


def start():

    sections = Section.objects()

    for section in sections:
        for city in City.objects:
            try:
                soup = get_page_soup(geo_id=city.city_id, section_id=section.section_id)
            except Exception as error:
                print(error)
                continue

            handle_notices(soup=soup, city_id=city.city_id)
            # break

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

    start()
