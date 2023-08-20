from dataclasses import dataclass
import pickle
import os
import logging
import filetype 
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class Photo:
    count: int
    last_used: int
    caption: str
    cid: str
    uri: str


class FileDBContextManager:
    def __init__(self, filename) -> None:
        self._filename: str = filename
        self._db: dict | None = None

    def init_db(self):
        logger.info("Creating a new one Database")
        self._db = dict()

    def __enter__(self):
        logger.debug("Loading from %s...", self._filename)
        try:
            self._db = pickle.load(open(self._filename, "rb"))
        except FileNotFoundError:
            logger.info("No database found, creating a new one")
            self.init_db()

        return self._db

    def __exit__(self, exc_type, exc_value, exc_tb):
        logger.debug("Saving to %s...", self._filename)
        pickle.dump(self._db, open(self._filename, "wb"))

class DatabaseError(Exception):
    pass

class Database:
    def __init__(self, filename="db.pickle", photos_dir="photos") -> None:
        self._filename: str = filename
        self._photos_dir: str = photos_dir
        self._db: FileDBContextManager = FileDBContextManager(filename)

    def sync_photos(self) -> None:
        with self._db as db:
            for photo in os.listdir(self._photos_dir):
                if f"{self._photos_dir}/{photo}" not in db:
                    if os.path.isdir(f"{self._photos_dir}/{photo}"):
                        logger.info(f"Skipping folder {photo}")
                        continue
                    ftype = filetype.guess(f"{self._photos_dir}/{photo}")
                    if ftype is None or not ftype.mime.startswith('image'):
                        logger.info(f"Skipping non-image file {photo}")
                        continue

                    logger.info(f"Adding new photo {photo}")
                    db[f"{self._photos_dir}/{photo}"] = Photo(
                        count=0, last_used=0, caption="", cid="", uri=""
                    )

            for photo in [
                db_photo
                for db_photo in db
                if db_photo.removeprefix(f"{self._photos_dir}/")
                not in os.listdir(self._photos_dir)
            ]:
                logger.info(f"Removing photo {photo}")
                del db[photo]

    def use_photo(self) -> tuple[str, Photo]:
        with self._db as db:
            if len(db) == 0:
                logger.error("No photos in database")
                raise DatabaseError("No photos in database")

            photos = list(db.keys())
            photos = sorted(photos, key=lambda x: db[x].count)

            db[photos[0]].count += 1
            db[photos[0]].last_used = datetime.now()

            return photos[0], db[photos[0]]

    def update_photo(self, photo, resp) -> None:
        with self._db as db:
            if photo not in db:
                logger.error(f"Photo {photo} not in database")
                raise DatabaseError(f"Photo {photo} not in database")

            db[photo].cid = resp.cid
            db[photo].uri = resp.uri

    def dump(self) -> None:
        with self._db as db:
            import pprint

            pprint.pprint(db)
