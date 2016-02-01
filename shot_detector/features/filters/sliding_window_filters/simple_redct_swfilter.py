# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import numpy as np

from scipy.fftpack import dct, dst, idct, idst


from .stat_swfilter import StatSWFilter

import math


import six
class SimpleReDCTSWFilter(StatSWFilter):
    """
        Implements 1D Fast Discrete COS transform.
        Only for experiment.
    """

    __logger = logging.getLogger(__name__)

    def aggregate_windows(self, window_seq, **kwargs):
        """
        Reduce sliding windows into values

        :param collections.Iterable[SlidingWindow] window_seq:
            sequence of sliding windows
        :param kwargs: ignores it and pass it through.
        :return generator: generator of sliding windows
        :rtype: collections.Iterable[SlidingWindow]
        """

        for window in window_seq:
            wlen = len(window)
            coef = wlen
            spectrum = dct(window)
            inverse_spectrum = idct(spectrum[:coef])
            for item in inverse_spectrum:
                result = item / (2 * wlen)
                for _ in xrange(wlen // coef):
                    yield result




