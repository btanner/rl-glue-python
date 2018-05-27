# 
# Copyright (C) 2007, Mark Lee
# 
# http://rl-glue-ext.googlecode.com/
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
#  $Revision$
#  $Date$
#  $Author$
#  $HeadURL$


import numpy as np


class RL_Abstract_Type(object):
    def __init__(self, num_ints=None, num_doubles=None, num_chars=None):
        self.int_array = []
        self.double_array = []
        self.char_array = []
        if num_ints is not None:
            self.int_array = np.zeros((num_ints,), dtype=int)
        if num_doubles is not None:
            self.double_array = np.zeros((num_doubles,), dtype=float)
        if num_chars is not None:
            self.char_array = np.chararray(num_chars)
            self.char_array[:] = ''

    def same_as(self, other_abstract_type):
        ints_same = self.int_array == other_abstract_type.int_array
        doubles_same = self.double_array == other_abstract_type.double_array
        chars_same = self.char_array == other_abstract_type.char_array
        return ints_same and doubles_same and chars_same

    # this coolness added by btanner sept 30/2008
    # it allows the subclasses to be used like myAction=Action.fromAbstractType(someAbstractType)
    @classmethod
    def from_abstract_type(cls, this_abstract_type):
        return_struct = cls()
        return_struct.int_array = np.copy(this_abstract_type.int_array)
        return_struct.double_array = np.copy(this_abstract_type.double_array)
        return_struct.char_array = np.copy(this_abstract_type.char_array)
        return return_struct


class Action(RL_Abstract_Type):
    def __init__(self, num_ints=None, num_doubles=None, num_chars=None):
        RL_Abstract_Type.__init__(self, num_ints, num_doubles, num_chars)


class Observation(RL_Abstract_Type):
    def __init__(self, num_ints=None, num_doubles=None, num_chars=None):
        RL_Abstract_Type.__init__(self, num_ints, num_doubles, num_chars)


class Observation_action(object):
    def __init__(self, the_obs=None, the_action=None):
        if the_obs is not None:
            self.o = the_obs
        else:
            self.o = Observation()
        if the_action is not None:
            self.a = the_action
        else:
            self.a = Action()


class Reward_observation_terminal(object):
    def __init__(self, reward=None, the_obs=None, terminal=None):
        if reward is not None:
            self.r = reward
        else:
            self.r = 0.0
        if the_obs is not None:
            self.o = the_obs
        else:
            self.o = Observation()
        if terminal is not None:
            self.terminal = terminal
        else:
            self.terminal = False


class Reward_observation_action_terminal(object):
    def __init__(self, reward=None, the_obs=None, the_action=None, terminal=None):
        if reward is not None:
            self.r = reward
        else:
            self.r = 0.0
        if the_obs is not None:
            self.o = the_obs
        else:
            self.o = Observation()
        if the_action is not None:
            self.a = the_action
        else:
            self.a = Action()
        if terminal is not None:
            self.terminal = terminal
        else:
            self.terminal = False
