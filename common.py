"""Include functions common for flask app and CIL app(meme)."""

import json
import os
import re
from datetime import datetime
from typing import List

import requests

from Helpers import Utilities as util
from MemeGenerator import MemeEngine
from Models import QuoteModel
from QuoteEngine import CustomErrors, Ingestor
from Services import QuoteToScrapScrapper


def load_quotestoscrap_quotes():
    """Get quotes from https://quotes.toscrape.com/.

    If there is no file with the quotes, scrap them and save in the file.
    The purpose is to have wilder quotes base to create better memes
    """
    local_storage = QuoteToScrapScrapper.DATA_STORAGE
    quotes = []

    def download(new_quotes):
        """Get quotes from the website."""
        try:
            new_quotes = QuoteToScrapScrapper.get_quotes()
            new_quotes = json.dumps([q.__dict__ for q in new_quotes])
            util.save_csv(new_quotes, local_storage)

        except requests.HTTPError as e:
            print(f"Somethong goes wrong\n{e.args[0]}")

        except requests.ConnectionError as e:
            print(
                  "Whoops, there is something wrong "
                  "with your internet connection. Don't worry! "
                  "There is a few quotes on board."
                  )

        else:
            print("Quotes ready....")

        finally:
            return quotes

    if not os.path.exists(local_storage):  # file does not exist
        print("Downloading more quotes for you to build more awersome memes.")
        download(quotes)

    else:
        try:
            quotes = Ingestor.parse(local_storage)

        except CustomErrors.UnsupportedFileError as e:
            print(e.msg)

        except CustomErrors.WrongFileStructureError as e:
            print(e.msg)

        finally:
            if not quotes:
                print("We need to refuel quotes. Please wait a while...")
                download(quotes)

    return quotes


def get_local_quotes(
                     data_storage: str = './_data',
                     excluded_dir: str = 'SimpleLines'
                     ) -> QuoteModel:
    """Get random quote from local files.

    Look for supported by 'IngestorInterface' files in specified catalog,
    collect all the found quotes and draw one of them to use in meme.
    :param data_storage: parent directory with quote files
    :data_storage type: str
    :param excluded_dir: subdir to exclude from the search process,
        default 'SimpleLines'
    :excluded_dir type: str, optional
    """
    supported_formats = Ingestor.get_supported_formats()
    quote_files = []

    for format in supported_formats:
        quote_files.extend(
            util.find_files_by_ext(
                base_dir=data_storage,
                extension=format,
                dir_to_exclude=excluded_dir
                )
            )

    quotes = []
    for f in quote_files:
        quotes.extend(Ingestor.parse(f))

    return quotes


def get_local_images(data_storage: str = './_data/photos') -> List[str]:
    """Collect path to all local images in data storage.

    Limit results to supported files only.
    :param data_storage: parent data directory
    :data_storage type: str
    :return: collection of paths to supported images
    :rtype: List[str]
    """
    image_paths = []

    for ext, format in MemeEngine.SUPPORTED_FORTMATS.items():
        image_paths.extend(
            util.find_files_by_ext(
                base_dir=data_storage, extension=ext
                )
            )

    return image_paths


def remove_temp_files(dir_path: str) -> None:
    """Clean unwanted temp files.

    :param dir_path: parent dir path
    :dir_path type: str
    """
    temp_regex = re.compile(r'^[\w,\s-]+\.[A-Za-z]{2,}$')
    files = util.find_files_by_ext(dir_path)

    files = \
        list(
            filter(
                lambda file: True if re.search(
                    temp_regex, util.get_filename(file))
                else False, files
                )
            )

    for file in files:
        os.remove(file)
        print(f"{file} has been removed...")


def remove_old_memes(dir_path: str, older_than: int = 172800) -> None:
    """Clean memes older than 48h.

    :param path: file path
    :dir_path type: str
    :param older_than = how many secounds from now should last
        to select the file to removal
    :older_than type: int
    """
    files = []
    print("Removing old files delegated to the separate process....")
    for format in MemeEngine.SUPPORTED_FORTMATS.keys():
        files.extend(util.find_files_by_ext(dir_path, format))

    now = datetime.now()
    files = \
        list(
             filter(
                    lambda file:
                    True if (
                        datetime.now()
                        - datetime.fromtimestamp(
                            os.path.getctime(file))).seconds
                    > older_than else False, files
                    )
             )

    for file in files:
        os.remove(file)
        print(f"{file} has been removed...")
