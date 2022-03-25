"""Download images from web."""
import requests
import pathlib
import os

from Helpers import Utilities as util
from Helpers import Validators
from requests.structures import CaseInsensitiveDict
from Services.Exceptions.InvalidUrlError import InvalidUrlError
from Services.Exceptions.UnsupportedImageError import UnsuportedImageError


class ImageDownloader():
    """Download image."""

    SUPPORTED_FORMATS = {'jpeg', "png"}

    @classmethod
    def download_bytes(cls, url: str) -> bytes:
        """Download image.

        :param url: image url
        :url type: str
        :raise HTTPError: response different than 2xx
        :raise ValueError: wrong url provided
        :raise ValueError: not an image downloaded
        :return: image represents by bytes
        :rtype: bytes
        """
        if not Validators.is_url(url):
            raise InvalidUrlError(f"Invalid url provided! {url}")

        try:

            result = requests.get(url, timeout=20)

        except requests.exceptions.Timeout:
            raise requests.HTTPError("Timeout error!")

        if result.status_code == 200:

            if not cls.is_supported:
                raise UnsuportedImageError(
                    "Not supported image or not image content!")

            return result.content

        else:
            raise requests.HTTPError(result.status_code)

    @classmethod
    def dowload_to_file(cls, url: str, path: str) -> str:
        """Download image and save it to file.

        :param url: image url
        :url type: str
        :param path: file path
        :path type: str
        :raise HTTPError: response different than 2xx
        :raise ValueError: wrong url provided
        :raise ValueError: not an image downloaded
        :return: image represents by bytes
        :rtype: bytes
        """
        byte_image = cls.download_bytes(url)
        return util.save_bytes(byte_image, path)

    @classmethod
    def is_supported(cls, res_headers: CaseInsensitiveDict) -> bool:
        """Check if the file is supported by the app.

        :param res_headers: response headers
        :res_headers type: `requests.Structures.CaseInsencitiveDict`
        :return: True if content-type header include supported format,
            otherwise False
        :rtype: bool
        """
        cont_type = res_headers.headers.get('content-type')

        if cont_type.lower().startswith("image"):
            img_type = cls.get_img_type(cont_type)

            if img_type in cls.SUPPORTED_FORMATS:
                return True
            else:
                return False

    @classmethod
    def get_img_type(cls, content_type: str) -> str:
        """Get file type.

        :param content-type: content of content-type response header
        :content-type type: str
        :return: type of the content (e.g. jpeg, png)
        :rtype: str
        """
        return content_type.split("/")[-1]
