# -*- coding: utf8 -*-

from __future__ import absolute_import

import numpy as np

from .base_compare_mixin import BaseCompareMixin

class SadMixin(BaseCompareMixin):

    def get_difference(self, curr_features, other_features, video_state, *args, **kwargs):
        '''
            FFMPEG-like method
            http://www.luckydinosaur.com/u/ffmpeg-scene-change-detector
            l1-norm, Also called «Manhattan norm»
        '''
        curr_vector =  np.array(curr_features) * 1.0

        #print curr_vector
        #1/0

        other_vector =  np.array(other_features) * 1.0
        diff_vector = np.abs(curr_vector - other_vector)
        sad = np.sum(diff_vector)
        colour_size, video_state = self.get_colour_size(
            curr_vector,
            video_state,
            *args,
            **kwargs
        )
        mean_sad = 1.0 * sad  / (diff_vector.size  * colour_size)
        return mean_sad, video_state
