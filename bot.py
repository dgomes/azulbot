from __future__ import annotations

import os
import logging
from atproto import Client
from atproto.xrpc_client.models.com.atproto.repo.create_record import Response

from const import IMAGE_ALT, DEFAULT_CAPTION

logger = logging.getLogger(__name__)


class Bot:
    def __init__(self, handle: str | None = None, password: str | None = None) -> None:
        self._handle = os.environ.get("BSKY_USERNAME") if handle is None else handle
        self._password = (
            os.environ.get("BSKY_PASSWORD") if password is None else password
        )
        self._client = Client()
        self._client.login(self._handle, self._password)

    def send_photo(
        self, path: str, caption: str | None, image_alt: str | None = None
    ) -> None:
        with open(path, "rb") as f:
            img_data = f.read()

            if not caption or caption == "":
                caption = DEFAULT_CAPTION
            if not image_alt or image_alt == "":
                image_alt = IMAGE_ALT

            logger.info(f"Sending photo {path} with caption {caption}")

            return Response(11, 22)
            response = self._client.send_image(
                text=caption, image=img_data, image_alt=image_alt
            )

            return response
