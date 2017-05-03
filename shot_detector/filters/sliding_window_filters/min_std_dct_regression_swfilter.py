# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function

import logging
import math

import numpy as np
from scipy.fftpack import dct

from .min_std_regression_swfilter import MinStdRegressionSWFilter


class MinStdDCTRegressionSWFilter(MinStdRegressionSWFilter):
    __logger = logging.getLogger(__name__)

    def aggregate_windows(self,
                          window_seq,
                          depth=0,
                          **kwargs):

        for window in window_seq:
            x_window = self.split(window, depth=depth, **kwargs)
            for index, item in enumerate(x_window):
                yield item

                # if index == 0:
                #     yield -0.1
                # else:
                #     yield item

    def replace_items(self, sequence, replacer=None, **kwargs):
        values = list(self.extract_values(sequence))

        values = list(self.dct_window(values))

        for index, item in enumerate(sequence):
            if not item.state:
                yield self.Atom(
                    index=item.index,
                    value=values[index],
                    state=True
                )
            else:
                yield item

    def dct_window(self,
                   window,
                   first=0,
                   last=None,
                   step=1,
                   **kwargs
                   ):
        window_len = len(window)
        if last is None:
            last = window_len
        spec_slice = slice(first, last, step)
        # noinspection PyArgumentEqualDefault
        spectrum = dct(window, type=2)
        spectrum = spectrum[spec_slice]
        for win_index, win_item in enumerate(window):
            i_spectrum_chain = (
                self.__norm(spec_index, window_len) * spec_item * np.cos(
                    math.pi * (2 * win_index - 1) * (spec_index) /
                    (2 * window_len)
                )
                for spec_index, spec_item in enumerate(
                spectrum
            )
            )
            regression_item = 2 * sum(i_spectrum_chain)
            yield regression_item

    @staticmethod
    def __norm(p, win_len):
        x = 2 if 0 == p else 1
        return 1 / (2 * x * win_len)
