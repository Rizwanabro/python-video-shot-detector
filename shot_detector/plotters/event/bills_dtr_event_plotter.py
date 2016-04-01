# -*- coding: utf8 -*-

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import logging

from shot_detector.filters import (
    DelayFilter,
    ShiftSWFilter,
    MeanSWFilter,
    NormFilter,
    StdSWFilter,
    DecisionTreeRegressorSWFilter
)

from shot_detector.utils.collections import SmartDict

from .base_event_plotter import BaseEventPlotter


class BillsDtrEventPlotter(BaseEventPlotter):

    __logger = logging.getLogger(__name__)

    def seq_filters(self):

        delay = DelayFilter()

        norm = NormFilter()

        shift = ShiftSWFilter(
            window_size=2,
            strict_windows=False,
            cs=False,
        )

        sad = delay(0) - shift

        mean = MeanSWFilter()

        std = StdSWFilter()

        def sigma3(c=3.0,**kwargs):
            return (
                delay(0) > (
                    mean(**kwargs)
                    + c*std(**kwargs)
                )
            ) | int

        dtr = DecisionTreeRegressorSWFilter(
            window_size=100,
            strict_windows=True,
            overlap_size=0,
            cs=False,
        )

        return [
            SmartDict(
                name='$F_{L_1} = |F_{t}|_{L_1}$',
                plot_options=SmartDict(
                    linestyle='-',
                    color='lightgray',
                    linewidth=3.0,
                ),
                filter=norm(l=1),
            ),
            SmartDict(
                name='$DTR_{300,2}$',
                plot_options=SmartDict(
                    linestyle='-',
                    color='red',
                    linewidth=2.0,
                ),
                filter=norm(l=1) | dtr(s=300, d=2)
            ),
            SmartDict(
                name='$S = '
                     '1/k\sum_{i=1}^{k} DTR_{i \cdot 25, 2} $',
                plot_options=SmartDict(
                    linestyle='-',
                    color='green',
                    linewidth=2.0,
                ),
                filter=norm(l=1) | sum(
                    [dtr(s=25*i+1) for i in xrange(1,9)]
                ) / 8
            ),
            SmartDict(
                name="$B_{50}/n = "
                     "(|S'| > |(\hat{\mu}_{50} "
                     "+ A \hat{\sigma}_{50})(S')|)"
                     "/n$",
                plot_options=SmartDict(
                    linestyle='-',
                    color='magenta',
                    linewidth=2.0,
                ),
                filter=norm(l=1) | sum(
                    [dtr(s=25*i+1) for i in xrange(1,9)]
                ) / 8 | (sad | abs) | sigma3(s=50) / 8
            ),
            SmartDict(
                name='$V(t) = '
                     '1/n\sum_{j=1}^{n} B_{j \cdot 25} $',
                plot_options=SmartDict(
                    linestyle=':',
                    color='blue',
                    linewidth=2.0,
                ),
                filter=norm(l=1) | sum(
                    dtr(s=25*i+1) for i in xrange(1,9)
                ) / 8 | (sad | abs) | sum(
                    sigma3(s=25*j) for j in xrange(1,9)
                ) / 8
            ),
        ]
