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


class TestMessageEnvironment(Environment):

    def env_init(self):
        return ""

    def env_start(self):
        return Observation()

    def env_step(self, action):
        return Reward_observation_terminal()

    def env_cleanup(self):
        pass

    def env_message(self, inMessage):
        if inMessage is None:
            return "null"

        if inMessage == "":
            return "empty"

        if inMessage == "null":
            return None

        if inMessage == "empty":
            return ""

        return inMessage


if __name__ == "__main__":
    EnvironmentLoader.load_environment(TestMessageEnvironment())
