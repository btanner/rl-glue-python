# 
# Copyright (C) 2008, Brian Tanner
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
#  $Revision$
#  $Date$
#  $Author$
#  $HeadURL$

from rlglue.environment.Environment import Environment
from rlglue.environment import EnvironmentLoader as EnvironmentLoader
from rlglue.types import Observation
from rlglue.types import Reward_observation_terminal


class TestEmptyEnvironment(Environment):
    whichEpisode = 0
    emptyObservation = Observation()
    nonEmptyObservation = Observation(2, 4, 5)

    def env_init(self):
        self.nonEmptyObservation.int_array = [0, 1]
        self.nonEmptyObservation.double_array = [0.0 / 4.0, 1.0 / 4.0, 2.0 / 4.0, 3.0 / 4.0]
        self.nonEmptyObservation.char_array = ['a', 'b', 'c', 'd', 'e']
        return ""

    def env_start(self):
        self.whichEpisode = self.whichEpisode + 1

        if self.whichEpisode % 2 == 0:
            return self.emptyObservation
        else:
            return self.nonEmptyObservation

    def env_step(self, action):
        ro = Reward_observation_terminal()

        if self.whichEpisode % 2 == 0:
            ro.o = self.emptyObservation
        else:
            ro.o = self.nonEmptyObservation

        return ro

    def env_cleanup(self):
        pass

    def env_message(self, inMessage):
        return None


if __name__ == "__main__":
    EnvironmentLoader.load_environment(TestEmptyEnvironment())
