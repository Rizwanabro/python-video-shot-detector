# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging

import numpy as np

from scipy.fftpack import dct, dst, idct, idst


from .stat_swfilter import StatSWFilter

import math

class FftSWFilter(StatSWFilter):
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
            coef = 10

            spectrum = dct(window, type=2)
            spectrum = spectrum[:coef]

            def a(p):
                if p == 0:
                    return 1 / (4 * wlen)
                return 1 / (2* wlen)

            for win_index, win_item in enumerate(window):
                regression_item = 2 * sum(
                    a(spec_index) * spec_item * np.cos(
                        math.pi * (2 * win_index - 1) * (spec_index) /
                        (2*wlen)
                    )
                    for spec_index, spec_item in enumerate(
                        spectrum[0:]
                    )
                )
                yield regression_item
