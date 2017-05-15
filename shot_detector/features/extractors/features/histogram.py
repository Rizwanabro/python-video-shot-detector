# -*- coding: utf8 -*-
"""
    This is part of shot detector.
    Produced by w495 at 2017.05.04 04:18:27
"""

from __future__ import absolute_import, division, print_function

from ..base_extractor import BaseExtractor


# noinspection PyAbstractClass
class Histogram(BaseExtractor):
    """
        ...
    """

    def frame_image_features(self, image_seq, **kwargs):
        """

        :type image_seq: collections.Iterable
        :param image_seq:
        :param kwargs:
        :return:
        """
        return self.colour_histogram(image_seq, **kwargs)
