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

from rlglue.agent.Agent import Agent
from rlglue.agent import AgentLoader as AgentLoader
from rlglue.types import Action


class TestEmptyAgent(Agent):
    whichEpisode = 0
    emptyAction = Action(0, 0, 0)
    nonEmptyAction = Action(7, 3, 1)

    def agent_init(self, taskSpec):
        self.whichEpisode = 0
        self.nonEmptyAction.int_array = (0, 1, 2, 3, 4, 5, 6)
        self.nonEmptyAction.double_array = (0.0 / 3.0, 1.0 / 3.0, 2.0 / 3.0)
        self.nonEmptyAction.char_array = ('a')

    def agent_start(self, observation):
        self.whichEpisode = self.whichEpisode + 1

        if self.whichEpisode % 2 == 0:
            return self.emptyAction
        else:
            return self.nonEmptyAction

    def agent_step(self, reward, observation):
        if self.whichEpisode % 2 == 0:
            return self.emptyAction
        else:
            return self.nonEmptyAction

    def agent_end(self, reward):
        pass

    def agent_cleanup(self):
        pass

    def agent_message(self, inMessage):
        return ""


if __name__ == "__main__":
    AgentLoader.load_agent(TestEmptyAgent())
