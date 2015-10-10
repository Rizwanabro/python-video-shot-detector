# -*- coding: utf8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import os

from shot_detector.utils.collections import SmartDict

from shot_detector.features.filters import BaseFilter, \
    MeanSWFilter, FactorFilter, NormFilter, DeviationDifferenceSWFilter, \
    ZScoreSWFilter, DeviationSWFilter, HistSimpleSWFilter, MedianSWFilter, BoundFilter, \
    StdSWFilter
from shot_detector.features.norms import L1Norm, L2Norm
from shot_detector.handlers import BaseEventHandler, BasePlotHandler

import datetime

PLAIN_FILTER_LIST = [
    SmartDict(
        skip=False,
        name='$F_i = |f_i|_{L_1}$',
        plot_options=SmartDict(
            linestyle='-',
            color='black',
            linewidth=1.0,
        ),
        subfilter_list=[
            (
                NormFilter(), SmartDict(
                    norm_function=L1Norm.length
                ),
            ),
        ],
    ),
    SmartDict(
        skip=False,
        offset=25,
        name='$M_i = median_{25}(F_j)$',
        plot_options=SmartDict(
            linestyle='-',
            color='gray',
            linewidth=2.0,
        ),
        subfilter_list=[
            (
                DeviationDifferenceSWFilter(), dict(
                    window_size=2,
                    std_coef=0,
                )
            ),
            (
                NormFilter(), SmartDict(
                    norm_function=L1Norm.length
                ),
            ),
        ],
    ),
    # SmartDict(
    #     skip=False,
    #     offset=50,
    #     name='$S_i = \sigma_{25} M_j$',
    #     plot_slyle='',
    #     plot_options=SmartDict(
    #         linestyle="-",
    #         color="green",
    #         linewidth=2.0,
    #     ),
    #     subfilter_list=[
    #         (
    #             NormFilter(), dict(
    #                 norm_function=L1Norm.length
    #             )
    #         ),
    #         (
    #             MedianSWFilter(), dict(
    #                 window_size=25,
    #                 sigma=-1,
    #                 flush_limit=-1,
    #                 window_limit=-1,
    #             )
    #         ),
    #         (
    #             StdSWFilter(), dict(
    #                 window_size=25,
    #                 flush_limit=-1,
    #                 window_limit=-1,
    #                 flush_trigger='point_flush_trigger',
    #             )
    #         ),
    #         (
    #             FactorFilter(), dict(
    #                 factor=2.0
    #             )
    #         )
    #     ],
    # ),
    #
    # SmartDict(
    #     skip=False,
    #     offset=60,
    #     step='E1',
    #     name='$E^{1}_{i} = \mu^{EWA}_{25} S_j$',
    #     plot_slyle='',
    #     plot_options=SmartDict(
    #         linestyle="-",
    #         color="blue",
    #         linewidth=1.0,
    #     ),
    #     subfilter_list=[
    #         (
    #             NormFilter(), dict(
    #                 norm_function=L1Norm.length
    #             )
    #         ),
    #         (
    #             MedianSWFilter(), dict(
    #                 window_size=25,
    #                 sigma=-1,
    #                 flush_limit=-1,
    #                 window_limit=-1,
    #             )
    #         ),
    #         (
    #             StdSWFilter(), dict(
    #                 window_size=25,
    #                 flush_limit=-1,
    #                 window_limit=-1,
    #                 flush_trigger='point_flush_trigger',
    #             )
    #         ),
    #         (
    #             MeanSWFilter(), dict(
    #                 mean_name='ewa',
    #                 window_size=10,
    #                 sigma=-1,
    #                 flush_limit=-1,
    #                 window_limit=-1,
    #             )
    #         ),
    #         (
    #             FactorFilter(), dict(
    #                 factor=2.0
    #             )
    #         )
    #     ],
    # ),
    #
    # SmartDict(
    #     skip=False,
    #     step='E2',
    #     offset=100,
    #     name='$E^{2}_{i} = \mu^{EWA}_{50} S_j$',
    #     plot_slyle='',
    #     plot_options=SmartDict(
    #         linestyle="-",
    #         color="purple",
    #         linewidth=1.0,
    #     ),
    #     subfilter_list=[
    #         (
    #             NormFilter(), dict(
    #                 norm_function=L1Norm.length
    #             )
    #         ),
    #         (
    #             MedianSWFilter(), dict(
    #                 window_size=25,
    #                 sigma=-1,
    #                 flush_limit=-1,
    #                 window_limit=-1,
    #             )
    #         ),
    #         (
    #             StdSWFilter(), dict(
    #                 window_size=25,
    #                 flush_limit=-1,
    #                 window_limit=-1,
    #                 flush_trigger='point_flush_trigger',
    #             )
    #         ),
    #         (
    #             MeanSWFilter(), dict(
    #                 mean_name='ewa',
    #                 window_size=50,
    #                 sigma=-1,
    #                 flush_limit=-1,
    #                 window_limit=-1,
    #             )
    #         ),
    #         (
    #             FactorFilter(), dict(
    #                 factor=2.0
    #             )
    #         )
    #     ],
    # ),
    #
    # SmartDict(
    #     skip=False,
    #     step='E1-E2',
    #     offset=100,
    #     name='$E^{1}_{i} - 3 \cdot E^{2}_{i} > 0$',
    #     plot_options=SmartDict(
    #         axvline=True,
    #         linestyle=":",
    #         color="teal",
    #         linewidth=1.0,
    #     ),
    #     subfilter_list=[
    #
    #     ],
    # ),
    #
    # SmartDict(
    #     skip=False,
    #     name='$Z_{Фишера} = \\frac{F_i - \mu_{100} F_j}{(\sigma_{100} S_k)} > 3$',
    #     plot_options=SmartDict(
    #         axvline=True,
    #         linestyle=":",
    #         color="red",
    #         linewidth=1.0,
    #     ),
    #     subfilter_list=[
    #         (
    #             NormFilter(), dict(
    #                 norm_function=L1Norm.length
    #             )
    #         ),
    #         (
    #             MedianSWFilter(), dict(
    #                 window_size=25,
    #                 sigma=-1,
    #                 flush_limit=-1,
    #                 window_limit=-1,
    #             )
    #         ),
    #         (
    #             StdSWFilter(), dict(
    #                 window_size=25,
    #                 flush_limit=-1,
    #                 window_limit=-1,
    #                 flush_trigger='point_flush_trigger',
    #             )
    #         ),
    #         (
    #             ZScoreSWFilter(), dict(
    #                 window_size=100,
    #                 sigma_num=3,
    #                 null_std=0,
    #                 flush_limit=-1,
    #                 window_limit=-1,
    #             )
    #         ),
    #         (
    #             FactorFilter(), dict(
    #                 factor=2000.0
    #             )
    #         )
    #     ]
    # ),
]


class BaseEventSelector(BaseEventHandler):
    __logger = logging.getLogger(__name__)

    plain_plot = BasePlotHandler()

    def plot(self, event, video_state, plotter, filter_list):
        for filter_desc in filter_list:
            if filter_desc.get('skip'):
                continue
            offset = filter_desc.get('offset', 0)
            step = filter_desc.get('step', None)
            base_filter = BaseFilter()
            filtered, video_state = base_filter.apply_subfilters(
                subfilter_list=filter_desc.subfilter_list,
                features=event.features,
                video_state=video_state,
            )

            if 'E1' == step:
                self.E1 = filtered
            if 'E2' == step:
                self.E2 = filtered
            if 'E1-E2' == step:
                filtered = 3000 * ((self.E1 - 3 * self.E2) > 0)


            if filtered:
                plotter.add_data(
                    filter_desc.name,
                    event.number,
                    filtered,
                    filter_desc.get('plot_slyle', ''),
                    **filter_desc.get('plot_options', {})
                )



        if 1.0 <= event.minute:
            plotter.plot_data()
            return

    def select_event(self, event, video_state=None, *args, **kwargs):

        """
            Should be implemented
        """

        point_flush_trigger = 'point_flush_trigger'
        event_flush_trigger = 'event_flush_trigger'


        self.plot(event, video_state, self.plain_plot, PLAIN_FILTER_LIST)

        now_datetime = datetime.datetime.now()
        diff_time = now_datetime - video_state.start_datetime
        print('  %s -- {%s}; [%s] %s' % (
            diff_time,
            event.number,
            event.hms,
            event.time,
        ))

        return [event], video_state
