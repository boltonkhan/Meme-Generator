"""Infractructure to draw caption on images."""

import pathlib
import textwrap
from random import choice
from string import ascii_letters
from typing import Dict, List, Tuple

from Helpers import Utilities as util
from Models.QuoteModel import QuoteModel
from PIL import Image, ImageDraw, ImageFont

from .Exeptions.TextTooLongError import TextTooLongError


class ImageCaptioner():
    """Generate caption for a given `PIL.Image` object.

    :data FONT_FORMAT: Accepted font format
    :FONT_FORMAT type: str
    :data DEF_FONTS_DIR: Parent dir with fonts files
    :DEF_FONTS_DIR type: str, default
    :data FONT_SIZE: A font size
    :FONT_SIZE type: int
    :data IMG_MARGIN: margin of the image
    :IMG_MARGIN type: float
    :data SPACING: interline for multiline text
    :SPACING type: int
    :param image: An image to draw text on
    :type image: 'PIL.Image' object
    :param quote: A quote/text to draw
    :type quote: `QuoteModel` object
    :param fonts_dir: Parent dir to look for fonts in
    :type fonts: str, optional
    :return: `ImageCaptioner` instance
    """

    FONT_FORMAT = ".ttf"
    DEF_FONTS_DIR = "_data/_fonts"
    FONT_SIZE = 22
    IMG_MARGIN = 0.07
    SPACING = 4

    def __init__(self, image: Image, quote: QuoteModel,
                 fonts_dir: str = DEF_FONTS_DIR
                 ) -> None:
        """Create an ImageCaptioner object."""
        self.image = image
        self.quote = quote

        self._canvas = self._get_canvas_size()

        self.fonts_dir = pathlib.Path(fonts_dir) \
            if fonts_dir != self.__class__.DEF_FONTS_DIR \
            else pathlib.Path(self.__class__.DEF_FONTS_DIR)

        self.set_font_style()

    def set_font_style(self) -> ImageFont:
        """Set random font path as an object field.

        :return: A font to draw text
        :rtype: `PIL.ImageFont` instance
        """
        fonts = self._get_fonts()
        chosen_font = self._select_font(fonts)

        self._font = \
            ImageFont.truetype(chosen_font, size=self.__class__.FONT_SIZE)

        return self._font

    def _get_canvas_size(self) -> int:
        """Return drawable size of the image.

        :return: drawable size of the image
        :rtype: tuple(int, int), first lenght, then height
        """
        margin_rate = 1 - self.__class__.IMG_MARGIN * 2

        canvas_width = int(self.image.size[0] * margin_rate)
        canvas_height = int(self.image.size[1] * margin_rate)

        return {"width": canvas_width, "height": canvas_height}

    def _get_fonts(self) -> List[str]:
        """Get paths to all found fonts in defined dir.

        :return: A collection of paths to found fonts
        :rtype: A list of str
        """
        fonts = util.find_files_by_ext(
            self.fonts_dir, self.__class__.FONT_FORMAT)
        assert fonts != []

        return fonts

    def _select_font(self, fonts: List[str]) -> str:
        """Choose a random font from the list.

        :param fonts: A collection of paths to fonts
        :type fonts: A list of str
        :return: A path to selected font
        :rtype: str
        """
        return choice(fonts)

    def run(self) -> Image:
        """Add a quote to the image.

        :return: An `PIL.Image` object with drawn caption
        :rtype: `PIL.Image`
        """
        self.quote.body = f"\"{self.quote.body}\""  # add `"` marks to body
        self.quote.author = f"-{self.quote.author}"  # add `-` mark to author

        text_to_draw = f"{self.quote.body} {self.quote.author}"

        text_size_pixels = \
            self._get_text_size(text_to_draw)  # text size in pixels

        if text_size_pixels[0] <= self._canvas["width"]:  # fit to one line
            pass  # leave text_text to draw in this format

        else:  # Doen not fit to one line

            author_size_pixel = \
                self._get_text_size(str(self.quote.author))  # author size

            body_size_pixel = \
                self._get_text_size(str(self.quote.body))  # body size

            wrap_width = \
                self._max_char_count(self._canvas["width"])  # max char count

            if body_size_pixel[0] <= self._canvas["width"]:  # if body fit
                text_to_draw = self.quote.body + "\n"  # draw body + new line

            if body_size_pixel[0] > self._canvas["width"]:  # body not fit
                text_to_draw = \
                    self._wrap_text(self.quote.body, wrap_width)  # wrap body

            if author_size_pixel[0] <= self._canvas["width"]:
                text_to_draw += \
                    self.quote.author  # author fits to the line

            if author_size_pixel[0] > self._canvas["width"]:  # author not fit
                wrap_width = self._max_char_count(self._canvas["width"])
                text_to_draw += \
                    self._wrap_text(self.quote.author, wrap_width)  # wrap

        final_text_size = self._get_text_size(text_to_draw)  # final text size

        if not self._is_enough_space(final_text_size):  # is text fits canvas
            raise TextTooLongError(
                "The quote doen't fit to the image size. "
                "It can be coused by the font style."
            )

        text_coord = \
            self._get_text_coord(final_text_size)  # random text coordinations

        self._draw_text_background(  # draw text backgroung
                                   final_text_size,
                                   text_coord
                                    )

        self._draw(text_to_draw, text_coord)  # # draw final text
        return self.image

    def _draw(self, text: str, text_coord: Dict) -> None:
        """Draw text on the image.

        Private method to encapsulate drawing text on the image.
        Check if the text is multiline or single line.
        :param text: text to draw
        :text type: str
        """
        # Set up font color
        rgb = self._get_most_common_color()
        rgb = self._invert_color(rgb)
        color = self._rgb_to_hex(rgb)

        draw = ImageDraw.Draw(im=self.image)

        if self._is_text_multiline(text):

            draw.multiline_text(xy=(text_coord["x"], text_coord["y"]),
                                text=text, font=self._font, fill=color,
                                spacing=self.__class__.SPACING
                                )

        else:
            draw.text(xy=(text_coord["x"], text_coord["y"]),
                      text=text, font=self._font, fill=color)

    def _is_text_multiline(self, text: str) -> bool:
        """Check if text is multiline.

        :param text: text to check
        :type text: str
        :return: True if text is multiline, otherwise False
        :rtype: bool
        """
        if text.find('\n') != -1:
            return True

        return False

    def _get_text_size(self, text: str) -> Tuple[int, int]:
        """Get size of the text in pixels.

        :param text: Text to measure
        :type text: str
        :return: With and height in pixels
        :rtype: tuple[int,int]
        """
        if self._is_text_multiline:
            return self._font.getsize_multiline(
                text, spacing=self.__class__.SPACING
            )

        return self._font.getsize(text)

    def _max_char_count(self, canvas_width: int) -> int:
        """Get max char count can be fitted to canvas with.

        :param canvas_width: Pixel count to use for drawing
        :canvas_width type: int
        :return: max char count fitted to canvas width
        :rtype: int
        """
        # Get avg width of ascii char for defined font
        avg_char_width = \
            sum(self._font.getsize(char)[0] for char in ascii_letters) \
            / len(ascii_letters)

        return util.round_up(canvas_width / avg_char_width)

    def _wrap_text(self, text: str, width_: int) -> str:
        r"""Wrap text to the width.

        :param text: Text to wrap
        :type text: str
        :param width: Max with of a single text line
        :type width: str
        :return: A wrapped text with `\n` as a new line
        :rtype: str
        """
        lines = textwrap.fill(text, width_)
        return lines + "\n"

    def _is_enough_space(self, text_size: Tuple[int, int]) -> bool:
        """Check if final text size is not bigger than canvas itself.

        :param text_size: Pixel width and pixel height of the text
            for defined font
        :text type: Tuplep[int, int]
        :return: True if text size is smaller than canvas, otherwise False
        :rtype: bool
        """
        if text_size[0] <= self._canvas["width"] \
                and text_size[1] <= self._canvas["height"]:

            return True

        return False

    def _get_text_coord(self, text_size: Tuple[int, int]) -> Dict:
        """Get random coordinates for the left upper corner of text.

        :param text_size: A text width and height in pixels.
        :text type: Tuple with two int values represent coordinates (x, y)
        :return: Randomply chosen coordinates
        :rtype: Dictionary with int coordinates with keys `x` and `y`
        """
        width_diff = self._canvas["width"] - text_size[0]
        height_diff = self._canvas["height"] - text_size[1]

        x_pos = choice(range(0, width_diff))
        y_pos = choice(range(0, height_diff))

        return {"x": x_pos, "y": y_pos}

    def _draw_text_background(self,
                              size: Tuple[int, int], pos: Dict) -> None:
        """Add half-opacity overlay as a background for the text.

        :param size: text size
        :size tyle: Tuple[int, int]
        :param pos: top-left corner of the text
        :pos type: Dict
        """
        padding = 1.05  # Add padding for the text

        re_size = tuple([int(x*padding) for x in size])  # recalculate size
        color = self._get_most_common_color()  # dominant image color

        overlay = Image.new('RGBA', re_size, color=color)  # create overlay

        overlay.putalpha(128)  # Add opacity

        # Adjust text position to padding
        offset = (re_size[0] - size[0], re_size[1] - size[1])
        position = (
             pos["x"] - int(offset[0] / 2), pos['y'] - int(offset[1] / 2))

        self.image.paste(overlay, position, overlay)

    def _get_most_common_color(self):
        """Get image colors sorted from the less common to the most common."""
        image = self.image.convert('RGB')
        colors = sorted(
            Image.Image.getcolors(
                image, maxcolors=self.image.size[0]*self.image.size[1]
                )
            )
        return colors[-2][1]

    def _invert_color(self, rgb: Tuple[int, int, int]
                      ) -> Tuple[int, int, int]:
        """Invert rbg color.

        :param rgb: color representation
        :rgb type: Tuple [int, int, int]
        :return: rgb coloe opposite to the provided
        :rtype: Tuple [int, int, int]
        """
        assert isinstance(rgb, Tuple)\
            and rgb[0] >= 0 and rgb[0] <= 255\
            and rgb[1] >= 0 and rgb[1] <= 255\
            and rgb[2] >= 0 and rgb[2] <= 255,\
            "Provided value has to be within a range 0 - 255"

        return tuple([255 - val for val in list(rgb)])

    def _rgb_to_hex(self, rgb: Tuple[int, int, int]) -> str:
        """Convert rgb to hex.

        :param rgb:  color representation
        :rgb type: Tuple [int, int, int]
        :return: hex representation
        :rtype: str
        """
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
