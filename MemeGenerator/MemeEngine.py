"""Module is responsible for manipulating images."""

import os
import pathlib
from typing import Tuple

from Helpers import Utilities as util
from Models import QuoteModel
from PIL import Image
from QuoteEngine.CustomErrors import UnsupportedFileError
from Services.Exceptions.UnsupportedImageError import UnsuportedImageError

from MemeGenerator.ImageCaptioner import ImageCaptioner
from MemeGenerator.ImageEnhancer import *


class MemeEngine():
    """Manipulate images.

    Open image, resize it, draw text and save as a new one
    :data SUPPOTED_FORMATS: Image formats/extensions digest by the class
    :SUPPOTED_FORMATS type: dict
        with full, start with period, extensions
    :data DEF_OUTPUT_DIR: folder to save the image
    :DEF_OUTPUT_DIR type: str
    :data MAX_WIDTH: max pixel count image can be resize to
    :MAX_WIDTH type: int
    :param output_dir: directory in which new generated
        image should be saved
    :output_dir tpe: str, optional
    """

    SUPPORTED_FORTMATS = {
        ".jpg": "JPEG",
        '.jpeg': "JPEG",
        ".png": "PNG"
    }

    DEF_OUTPUT_DIR = "_data/memes"
    MAX_WIDTH = 500

    def __init__(self, output_dir: str = DEF_OUTPUT_DIR) -> None:
        """Create an instance."""
        self.output_dir = output_dir
        self.meme_path = None

    @property
    def enhancer(self):
        """Get value of enhancer field."""
        if not self.__dict__.get("_enhancer"):
            self._enhancer = None
        return self._enhancer

    @enhancer.setter
    def enhancer(
                self, enhancer: ImageEnhancerInterface) -> Image:
        """Select enhancer.

        :param enhancer: enhancement method
        :enhancer type: `ImageEnhancerInterface`
        :return: `ImageEnhancerInterface` class
        :rtype: `ImageEnhancerInterface`
        """
        self._enhancer = enhancer

    def make_meme(self, img_path: str, text: str,
                  autor: str, width: int = MAX_WIDTH) -> str:
        """Generate meme.

        Open, resize, draw text and save transformed image.
        :param img_path: A path to the image file
        :img_path type: str
        :param text: Text/quote to draw
        :text type: str
        :param: author: An author of the text
        :author type: str
        :param width: Desired width of the image (default: 500px)
        :width type: int
        :return: A path/location to/of transformed image
        :rtype: str
        """
        img_path = pathlib.Path(img_path)
        image = self._open_image(img_path)  # open image
        image = self._resize_image(image, width)  # resize image

        if self.enhancer is not None:
            image = self.enhancer.enhance(image)

        captioned_image = ImageCaptioner(
            image, QuoteModel(text, autor)).run()  # add text to image

        name_lenght = 10  # lenght of a file name
        file_name = \
            util.build_random_str(name_lenght) + '.png'  # build file name

        pathlib.Path(self.output_dir).mkdir(
            parents=True, exist_ok=True)  # create dir if not exists
        save_path = os.path.join(self.output_dir, file_name)  # build full path

        self.__class__.save_image(captioned_image, save_path)  # save image
        self.meme_path = save_path
        return save_path  # return file path

    @classmethod
    def is_supported(cls, filename: str) -> bool:
        """Check if the file is supported by MemeEngine.

        :param filename: filename to check
        :filename type: str
        :return: True if is supported, otherwise False
        :rtype: bool
        """
        ext = util.get_extension(filename)

        if ext in cls.SUPPORTED_FORTMATS:
            return True
        False

    def _open_image(self, img_path: str) -> Image:
        """Open an image using given location.

        :param img_string:A path to the image file
        :img_string type: str
        :return: `PIL.Image` object
        :exceptions: `UnsupportedFileError`
            raises if file format is not supported
        """
        # Get the file extension.
        extension = util.get_extension(img_path)

        # Check if can digest the file.
        if extension not in self.SUPPORTED_FORTMATS.keys():
            raise UnsuportedImageError(
                f"Failed to open image: {img_path}. Unsupported type."
            )
        return Image.open(img_path)

    @classmethod
    def save_image(cls, image: Image, file_name: str) -> None:
        """Save image.

        :param image: image to save
        :image type: `PIL.Image`
        :param file_name: file name
        :file_name type: str
        """
        image.save(file_name)

    def _get_new_size(self, size: Tuple[int, int],
                      width: int) -> Tuple[int, int]:
        """Calculate new image size aligning to defined width.

        :param size: width and height of image
        :size type: A tuple of int
        :param width: expeted width
        :width type: int
        :return: tuple(int, int): new image size, max 500
        """
        if width > MemeEngine.MAX_WIDTH:
            width = MemeEngine.MAX_WIDTH

        return tuple([int(d * (width / size[0])) for d in list(size)])

    def _resize_image(self, image: Image, width: int) -> Image:
        """Resize image.

        :param image: An image to resize
        :image type: `PIL.Image`
        :param width: width to image resize to
        :width type: int
        :return: Resized image
        :rtype: `PIL.Image`
        """
        new_size = self._get_new_size(image.size, width)
        return image.resize(new_size)
