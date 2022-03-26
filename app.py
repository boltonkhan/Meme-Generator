"""Flask version of meme app."""

import atexit
import multiprocessing
import os
import pathlib
import random

import requests
from flask import Flask, redirect, render_template,\
                  request, send_file, url_for

import common
from Helpers import ExLogger
from Helpers import Utilities as util
from MemeGenerator import MemeEngine
from MemeGenerator.Exeptions.TextTooLongError import TextTooLongError
from Models.QuoteModel import QuoteModel
from Services import GoodReadScrapper, UnsplashService
from Services.Exceptions.InvalidUrlError import InvalidUrlError
from Services.Exceptions.UnsupportedImageError import UnsuportedImageError
from Services.ImageDownloader.ImageDownloader import ImageDownloader


error_msgs = {
    'text_to_long': 'Text is to long. '
    'Try to make it shorter (max 300 chars in total).',
    'not_filled': 'All fields must be filled!',
    'not_url': 'Provide valid url!',
    'unsupported_img': 'Not supported image or not image content!'
}

storage = '_data/memes'
tmp = '_data/memes/tmp/'
static_url = f"/{storage}"

app = Flask(__name__,
            static_url_path=static_url,
            static_folder=storage)

meme = MemeEngine(storage)


def get_online_quotes():
    """Load quote resources and draw the quote."""
    quotes = common.get_local_quotes()

    try:
        online_quotes = GoodReadScrapper.get_quotes()

    except requests.HTTPError as e:
        ExLogger().log(e)

    except ConnectionError as e:
        ExLogger().log(e)

    finally:
        if online_quotes:
            quotes = random.choice([quotes, online_quotes])

    return quotes


def get_unsplash_image():
    """Get 5 new images from unsplash service."""
    service = UnsplashService(storage_path=tmp)
    un_images = service.get_random(count=1)
    if not un_images or not un_images[0].local_path:
        raise ValueError(
            "Something went wrong downloading unsplash image.")
    return un_images[0].local_path


def setup():
    """Load all resources."""
    quotes = common.get_local_quotes()
    images = common.get_local_images()

    return quotes, images


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Generate a random meme."""
    img = random.choice(imgs)
    quote = random.choice(quotes)

    try:
        path = meme.make_meme(img, quote.body, quote.author)
    except TextTooLongError:
        return redirect(url_for('meme_rand'))

    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user defined meme."""
    if request.method == 'POST':
        result = request.form

        try:
            url = result["image_url"]
            body = result["body"]
            author = result["author"]
            quote = QuoteModel(body, author)

            if not url or not body or not author:
                raise ValueError('All fields must be filled!')

            filename = \
                f"{util.build_random_str(4)}{util.get_extension(url)}"

            temp_img = os.path.join(tmp, filename)
            temp_img = ImageDownloader.dowload_to_file(url, temp_img)

            path = meme.make_meme(temp_img, quote.body, quote.author)

        except AssertionError as e:
            # error = error_msgs['text_to_long']
            error = str(e)

        except TextTooLongError as e:
            # error = error_msgs['text_to_long']
            error = str(e)

        except InvalidUrlError as e:
            # error = error_msgs['not_url']
            error = str(e)

        except UnsuportedImageError as e:
            # error = error_msgs['unsupported_img']
            error = str(e)

        except ValueError as e:
            # error = error_msgs['not_filled']
            error = e.args[0] if e.args else \
                "Something gone wrong. Meybe you didn't fill all fields?"

        except requests.HTTPError as e:
            error = e.args[0] if e.args else \
                "Something gone wrong with the connection."

        except ConnectionError as e:
            error = e.args[0] if e.args else \
                "Something gone wrong with the connection."

        else:
            return render_template('meme.html', path=path)

    return render_template('meme_form.html', error=error)


@app.route('/unsplash-create', methods=["GET"])
def unsplash_form():
    """Get random image from unsplash API and let the user create meme."""
    try:
        path = get_unsplash_image()

    except AssertionError as e:
        error = e. args[0] if len(e.args) > 0 else "Unknown error occured."
        return render_template('base.html', error=error)

    except requests.HTTPError as e:
        error = e. args[0] if len(e.args) > 0 else "Unknown error occured."
        return render_template('base.html', error=error)

    except ConnectionError as e:
        error = e.args[0] if e.args else \
            "Something gone wrong with the connection."
        return render_template('base.html', error=error)

    else:
        if os.path.exists(path):
            return render_template('unsplash_form.html', path=path)

    redirect(url_for('unsplash_form'))


@app.route('/unsplash-create', methods=["POST"])
def unsplash_post():
    """Create user defined meme for a random selected unsplash photo."""
    if request.method == 'POST':
        result = request.form

        try:
            img_path = result["img_path"]
            body = result["body"]
            author = result["author"]

            if not body or not author:
                raise ValueError('All fields must be filled!')

            quote = QuoteModel(body, author)

            path = meme.make_meme(img_path, quote.body, quote.author)

        except AssertionError as e:
            error = e.args

        except TextTooLongError:
            error = error_msgs['text_to_long']

        except InvalidUrlError:
            error = error_msgs['not_url']

        except UnsuportedImageError:
            error = error_msgs['unsupported_img']

        except ValueError:
            error = error_msgs['not_filled']

        except FileNotFoundError:
            return redirect(url_for('unsplash_form'))

        except ConnectionError as e:
            error = e.args[0] if e.args else \
                "Something gone wrong with the connection."
            return render_template('base.html', error=error)

        else:
            return render_template('meme.html', path=path)

        if os.path.exists(img_path):
            return render_template('unsplash_form.html',
                                   path=img_path, error=error)
        else:
            return redirect(url_for('unsplash_form'))


@app.route('/download', methods=['GET'])
def download():
    """Download photo using browser."""
    if meme.meme_path:
        return send_file(meme.meme_path, as_attachment=True)
    return redirect(url_for('meme'))


if __name__ == "__main__":

    # delete ald files
    p = multiprocessing.Process(
        target=common.remove_old_memes, args=(f"{storage}",))
    p.daemon = True
    p.start()

    # delete temp file when application will be stopped
    atexit.register(common.remove_temp_files, dir_path=tmp)

    app.run()
