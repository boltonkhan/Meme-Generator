"""Run console version of Meme Generator."""

import argparse
import atexit
import multiprocessing
import os
import pathlib
import random
from secrets import choice
from typing import List

import requests
from QuoteEngine.CustomErrors import UnsupportedFileError
from Services.Exceptions.UnsupportedImageError import UnsuportedImageError

import common
from Helpers import Utilities as util
from MemeGenerator import MemeEngine
from MemeGenerator.ImageEnhancer import (BrightnessImageEnhancer,
                                         ColorImageEnhancer,
                                         ContrastImageEnhancer,
                                         SharpnessImageEnhancer)
from Models import QuoteModel
from Services import ImageDownloader, UnsplashService
from Services.QuoteScrapper.GoodReadScrapper import GoodReadScrapper


data_storage = './_data'
default_dir = f"{data_storage}/memes"
tmp_dir = f"{default_dir}/tmp"


def generate_meme(
        path=None, url=None, unsplash=None,
        body=None, author=None, goodread=None, enhance=None
        ):
    """Generate a meme given an path and a quote.

    :param path: image path, default random
    :path type: str, optional
    :param url: url to image
    :url type: str
    :param unsplash: if selected, random image from unsplash API
        will be used
    :unsplash type: bool
    :param body: text to draw, default random
    :body type: str, optional
    :param author: text author, default random
    :author type: str, optional
    :param goodread: if selected, 'https://www.goodreads.com/' random
        page will be scrapped and random quote will be selected
    :goodread type: bool
    :param enhance: random enhancer (color, contrast, sharpness, brightness)
        will be selected and add to the picture with random factor
    :enhance type: bool
    :return: path to generated file

    :rtype: str
    """
    img_path = None
    quote = None
    enhancer = None

    """Section responsible for selecting image/ image path"""
    if not path and not url and not unsplash:  # random image
        image_paths = common.get_local_images()
        img_path = random.choice(image_paths)

    elif path and not url and not unsplash:  # local image
        img_path = path

    elif url and not path and not unsplash:  # img from url
        filename = \
            f"tmp_{util.build_random_str(4)}{util.get_extension(url)}"
        path = os.path.join(tmp_dir, filename)

        img_path = ImageDownloader.dowload_to_file(url=url, path=path)

    elif unsplash and not url and not path:  # image from unsplash API
        service = UnsplashService()

        images = service.get_random(count=1)

        if len(images) == 1:
            if images[0].local_path is not None:
                img_path = images[0].local_path
        else:
            raise ValueError("No image data found!")

    else:  # can't mix attributes
        raise ValueError(
                         "Only one attribute from following: "
                         "path, url or unsplash can be selected!"
                         )

    """Section responsible for selecting quote"""
    if not body and not author and not goodread:  # random local quote
        quotes = common.get_local_quotes(data_storage)
        quote = choice(quotes)

    elif goodread and not body and not author:  # goodread quote
        quotes = GoodReadScrapper.get_quotes()
        quote = random.choice(quotes)

    elif not goodread and body and author:  # use user input
        quote = QuoteModel(body, author)

    else:
        raise ValueError(
            "If goodread is selected, body and author can't be used. "
            "If you chose to use your text, "
            "please fill both the body and the author."
            )

    if enhance:  # add enhancer

        enhancers = [
            BrightnessImageEnhancer,
            SharpnessImageEnhancer,
            ColorImageEnhancer,
            ContrastImageEnhancer
        ]

        enhancer = choice(enhancers)

    meme = MemeEngine(pathlib.Path(default_dir))
    path = meme.make_meme(img_path, quote.body, quote.author)

    return path


if __name__ == "__main__":
    """Run the program in the command line.

    :param --path: image path
    :path type: str, optional
    :param --body: text to draw
    :body type: str, optional
    :param author: text author
    :author type: str, optional
    """
    p = multiprocessing.Process(
        target=common.remove_old_memes, args=(default_dir,))
    p.daemon = True
    p.start()

    atexit.register(common.remove_temp_files, dir_path=tmp_dir)

    parser = argparse.ArgumentParser()

    parser.add_argument(
                        "--path",
                        help="Optional: local path to the image."
                             "Can't be used with unsplash or url. "
                             "Only one parameter can be used.",
                        type=str
                        )

    parser.add_argument(
                        "--url",
                        help="Optional: Image url you want to use for meme. "
                             "Can't be used with unsplash or path. "
                             "Only one parameter can be used.",
                        type=str
                        )

    parser.add_argument(
                        "--unsplash",
                        help="Optional: use with no value. "
                             "If selected random image from unsplash API "
                             "will be used. Can't be used with unsplash "
                             "or url. Only one parameter can be used.",
                        action="store_true"
                        )

    parser.add_argument(
                        "--body",
                        help="Optional: quote to draw. "
                             "If body is given, author is required.",
                        type=str
                        )

    parser.add_argument(
                        "--author",
                        help="Optional: author of the quote. "
                             "If author is given, body is required.",
                        type=str
                        )

    parser.add_argument(
                        "--goodread",
                        help="Optional: use with no value."
                             "Can't be selected if manual input "
                             "(body and author) is used.",
                        action="store_true"
                        )

    parser.add_argument(
                        "--enhance",
                        help="Optional: use with no value."
                             "Random image enhancement: contrast, brightness,"
                             "sharpness, color.",
                        action="store_true"
                        )

    args = parser.parse_args()
    common.load_quotestoscrap_quotes()
    path = None

    try:
        path = generate_meme(
            path=args.path,
            url=args.url,
            unsplash=args.unsplash,
            body=args.body,
            author=args.author,
            goodread=args.goodread,
            enhance=args.enhance
        )
    except UnsuportedImageError as e:
        print(e)

    except UnsupportedFileError as e:
        print(e)

    except AssertionError as e:
        print(e)

    except ValueError as e:
        print(e)

    except requests.HTTPError as e:
        print(f"Somethong goes wrong\n{e.args[0]}")

    except requests.ConnectionError:
        print(
            "Whoops, there is something wrong "
            "with your internet connection. Just generate meme "
            "from we've got."
            )
    else:
        print(path)
