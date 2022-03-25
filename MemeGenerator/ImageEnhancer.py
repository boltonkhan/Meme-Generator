"""Enhance image changing its colors."""

from abc import ABC, abstractmethod

from Helpers import Utilities as util
from PIL import Image, ImageEnhance


class ImageEnhancerInterface(ABC):
    """Provides infracture interface to enhance image."""

    @classmethod
    @abstractmethod
    def enhance(cls, image: Image, factor: float) -> Image:
        """Enhance given Image interface.

        :param image: An image to enhance
        :image type: `PIL.Image`
        :param factor: The factor changes the brithness of the image.
            1 is an original image brightness. 0 dark image,
            values above 1 make the image brigther
        :factor type: float
        :return: transformed image
        :rtype: `PIL.Image`
        """
        pass


class BrightnessImageEnhancer(ImageEnhancerInterface):
    """Provides methods for adjust image brightness."""

    @classmethod
    def enhance(cls, image: Image,
                factor: float = util.draw_float(0.4, 0.8)
                ) -> Image:
        """Adjust brightness of the image.

        :param image: An image to enhance
        :image type: `PIL.Image`
        :param factor: The factor changes the brithness of the image.
            1 is an original image brightness. 0 dark image,
            values above 1 make the image brigther,
            default random number from 0.4 to 0.8
        :factor type: float, optional
        :return: transformed image
        :rtype: `PIL.Image`
        """
        assert isinstance(factor, float) and factor >= 0
        filter = ImageEnhance.Brightness(image)

        return filter.enhance(factor)


class ColorImageEnhancer(ImageEnhancerInterface):
    """Provides methods for adjust image brightness."""

    @classmethod
    def enhance(cls, image: Image,
                factor: float = util.draw_float(0.2, 0.8)
                ) -> Image:
        """Adjust color of the image.

        :param image: An image to enhance
        :image type: `PIL.Image`
        :param factor: The factor changes the color of an image
            1.0 is an original image, 0.0 is a black and white image,
            default random value from 0.2 to 0.8
        :factor type: float, optional
        :return: transformed image
        :rtype: `PIL.Image`
        """
        assert isinstance(factor, float) and factor >= 0
        filter = ImageEnhance.Color(image)

        return filter.enhance(factor)


class ContrastImageEnhancer(ImageEnhancerInterface):
    """Provides methods for adjust image contrast."""

    @classmethod
    def enhance(cls, image: Image,
                factor: float = util.draw_float(0.0, 1.0)
                ) -> Image:
        """Adjust contrast of the image.

        :param image: An image to enhance
        :image type: `PIL.Image`
        :param factor: The factor changes the color of an image
            1.0 is an original image, 0.0 solid grey image
            defaults random from 0.0 to 1.0
        :factor type: float, optional
        :return: transformed image
        :rtype: `PIL.Image`
        """
        assert isinstance(factor, float) and factor >= 0
        filter = ImageEnhance.Contrast(image)

        return filter.enhance(factor)


class SharpnessImageEnhancer(ImageEnhancerInterface):
    """Provides methods for adjust image sharpness."""

    @classmethod
    def enhance(cls, image: Image,
                factor: float = util.draw_float(0.0, 4.0)
                ) -> Image:
        """Adjust sharpness of the image.

        :param image: An image to enhance
        :image type: `PIL.Image`
        :param factor: The factor changes the sharpness of an image
            1.0 is an original image. 0.0 blurred image,
            values above 1 make the image sharpened,
            defaults random value from 0.0 to 4.0
        :factor type: float, optional
        :return: transformed image
        :rtype: `PIL.Image`
        """
        assert isinstance(factor, float) and factor >= 0
        filter = ImageEnhance.Sharpness(image)

        return filter.enhance(factor)
