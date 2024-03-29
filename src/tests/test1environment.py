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
#
#  $Revision$
#  $Date$
#  $Author$
#  $HeadURL$


from rlglue.environment.Environment import Environment
from rlglue.environment import EnvironmentLoader as EnvironmentLoader
from rlglue.types import Observation
from rlglue.types import Reward_observation_terminal


class Test1Environment(Environment):
    stepCount = 0
    o = Observation()

    def env_init(self):
        return "sample task spec"

    def env_start(self):
        self.stepCount = 0

        self.o.int_array = [1]
        self.o.double_array = [0.0 / 2.0, 1.0 / 2.0]
        self.o.char_array = ['a', 'b', 'c']

        return self.o;

    def env_step(self, action):
        ro = Reward_observation_terminal()
        terminal = False

        if self.stepCount < 5:
            self.o.double_array = []
            self.o.char_array = []
            self.o.int_array = [self.stepCount]

            self.stepCount = self.stepCount + 1

            if self.stepCount == 5:
                terminal = True

            ro.r = 1.0

        else:
            self.o.double_array = [0.0078125, -0.0078125, 0.0, 0.0078125e150, -0.0078125e150]
            self.o.char_array = ['g', 'F', '?', ' ', '&']
            self.o.int_array = [173, -173, 2147483647, 0, -2147483648]

            ro.r = -2.0

        ro.o = self.o
        ro.terminal = terminal
        return ro

    def env_cleanup(self):
        pass

    def env_message(self, inMessage):
        timesToPrint = self.stepCount % 3

        outMessage = inMessage + "|"
        for i in range(0, timesToPrint):
            outMessage = outMessage + "%d" % (self.stepCount)
            outMessage = outMessage + "."

        outMessage = outMessage + "|" + inMessage

        return outMessage


if __name__ == "__main__":
    EnvironmentLoader.load_environment(Test1Environment())
