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


class TestSpeedEnvironment(Environment):
    stepCount = 0
    whichEpisode = 0
    o = Observation()

    def env_init(self):
        return ""

    def env_start(self):
        self.stepCount = 0
        self.whichEpisode = self.whichEpisode + 1

        return Observation()

    def env_step(self, action):
        self.stepCount = self.stepCount + 1

        if self.whichEpisode % 2 == 0:
            self.o.int_array = range(0, 50000)
            # cheating, might break something
            self.o.double_array = range(0, 50000)
            terminal = 0
            if self.stepCount == 200:
                terminal = 1
            ro = Reward_observation_terminal()
            ro.r = 1.0
            ro.o = self.o
            ro.terminal = terminal
            return ro

        self.o.int_array = range(0, 5)
        # cheating, might break something
        self.o.double_array = range(0, 5)
        terminal = 0
        if self.stepCount == 5000:
            terminal = 1
        ro = Reward_observation_terminal()
        ro.r = 1.0
        ro.o = self.o
        ro.terminal = terminal
        return ro

    def env_cleanup(self):
        pass

    def env_message(self, inMessage):
        return None;


if __name__ == "__main__":
    EnvironmentLoader.load_environment(TestSpeedEnvironment())
