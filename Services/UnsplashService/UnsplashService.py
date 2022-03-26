"""Download images using usplash API.

API url: https://unsplash.com/
API documentation: https://unsplash.com/documentation
"""
import http
from itertools import count
import json
import requests
import pathlib
import random

from Services.ImageDownloader.ImageDownloader import ImageDownloader
from Helpers import Utilities as util
from Services.ServiceConfig.ServiceConfig import ServiceConfig
from typing import List


class UnsplashModel():
    """Represent the single image object downloaded from unsplash.

    :param img_id: image id
    :img_id type: str
    :param image_urls: image url to use in the internet,
        according to API policy this urls should be used on websites
    :image_ulrs type: List[str]
    :param download_url: url to download image from
    :download_url type: str
    """

    def __init__(
        self, img_id: str, image_url: str, download_url: str
                ) -> None:
        """Construct the object."""
        self.img_id = img_id
        assert self.img_id is not None

        self.image_url = image_url
        assert self.image_url is not None

        self.download_url = download_url
        assert self.download_url is not None

    @property
    def local_path(self) -> str:
        """Get local path to downloaded image."""
        if not self.__dict__.get("_local_path"):
            self._local_path = None
        return self._local_path

    @local_path.setter
    def local_path(self, local_path: str) -> None:
        """Set local path for downloaded image."""
        self._local_path = local_path

    def __str__(self):
        """Return string object representation."""
        return f"Id: {self.img_id}\nURL: {self.image_url}" \
               f"\nDOWNLOAD: {self.download_url}\nLocal Path: " \
               f"{self.local_path}"


class UnsplashService():
    """Download images using usplash API.

    :data BASE_URL: base api url
    :BASE_URL type: str
    :data STORAGE: path to the local dir with unsplash images
    :STORAGE type: str
    :data DEF_CONF_FILE: default location of the config file
    :DEF_CONF_FILE type: str
    :param config_path: path to the config file includes `api key`
    :config_path type: str
    """

    BASE_URL = "https://api.unsplash.com/"
    STORAGE = "_data/photos/unsplash/"
    DEF_CONF_FILE = "_config_files/unsplash_config.json"

    def __init__(self, config_path: str = DEF_CONF_FILE,
                 storage_path: str = STORAGE) -> None:
        """Create an object."""
        self.config = self._load_config(config_path)

        assert self.config is not None,\
            "Invalid unsplash configuration file." \
            " Must exists and be valid json file."

        if self.config:
            assert self.config.api_key is not None,\
                "Config file does not contain a valid api_key!"

        self.storage_path = storage_path

    def get_random(self, count=5):
        """GET {base_url}/photos/random."""
        end_url = '/photos/random'
        request_url = ''.join([self.__class__.BASE_URL, end_url])
        payload = {
            "count": count
        }
        headers = {
            "Accept-Version": "v1",
            "Authorization": "Client-ID " + self.config.api_key
        }
        images = []

        res = requests.get(request_url, headers=headers, params=payload)

        if res.status_code == 200:
            data = res.json()

            images = list(  # transform to UnsplashModel
                map(self._map_to_unsplashmodel, data)
            )

            images = self._find_existed(images)  # update path for existed
            images = self._download_not_existed(images)  # download new

            return images

        else:
            result = json.loads(res.content)
            error_msg = "\n".join(result.get("errors"))
            raise requests.HTTPError(error_msg)

    def _find_existed(
            self, imgs: List[UnsplashModel]) -> List[UnsplashModel]:
        """Check if the image is not in the storage yet.

        If exists, add the path to the image.
        """
        files = util.find_files_by_ext(self.storage_path)

        for im in imgs:
            for file in files:
                if file.count(im.img_id) > 0:
                    im.local_path = file

        return imgs

    def _download_not_existed(
            self, imgs: List[UnsplashModel]) -> List[UnsplashModel]:
        """Get images not in the storage currently.

        :param images: collection of got images from API
        :images type: `List[UnsplashImageModel]`
        :return: collection of images with local paths
        :rtype: `List[UnsplashImageModel]`
        """
        for im in imgs:

            if not im.local_path:

                type = \
                    util.param_value_from_url('fm', im.image_url)  # img type
                filename = '.'.join([im.img_id, type])  # image type plus id
                path = ''.join([self.storage_path, filename])

                down_img = ImageDownloader.dowload_to_file(  # download file
                    url=im.download_url, path=path
                )

                im.local_path = path

        return imgs

    def _load_config(self, config_path: str) -> ServiceConfig:
        """Load service config file.

        :param config_path: path to the file
        :config_file type: str
        """
        return ServiceConfig.create(config_path)

    def _map_to_unsplashmodel(self, res_content: json) -> UnsplashModel:
        """Map response to `UnsplashImageModel`.

        :param res_content: api response
        :res_content type: json
        :return: image details like id, url etc.
        :rtype: `UnsplashImageModel`
        """
        return UnsplashModel(
            img_id=res_content.get('id', None),
            image_url=res_content.get('urls', None).get('small', None),
            download_url=res_content.get('links', None).get('download', None)
        )
