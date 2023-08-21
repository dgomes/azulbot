import logging
import os
import sys
import argparse

from db import Database, DatabaseError
from bot import Bot
from const import DB_FILE, PHOTOS_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(args):
    db = Database(DB_FILE, PHOTOS_DIR)
    if args.sync:
        print("Syncronizing database with imagedir")
        db.sync_photos()

    elif args.dump:
        print("Dumping database")
        db.dump()

    else:
        bot = Bot()
        try:
            photo, metadata = db.get_photo()
        except DatabaseError:
            logger.error("No photos available")
            return 1
        resp = bot.send_photo(path=photo, caption=metadata)
        db.update_photo(photo, resp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AzulBot - Blue Sky Image Bot")
    parser.add_argument(
        "--sync", help="syncronize imagedir with database", action="store_true"
    )
    parser.add_argument("--dump", help="dump database", action="store_true")
    parser.add_argument("--replies", help="syncronize replies", action="store_true")

    args = parser.parse_args()
    sys.exit(main(args))
