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


class TestMessageAgent(Agent):
    whichEpisode = 0

    def agent_init(self, taskSpec):
        pass

    def agent_start(self, observation):
        return Action()

    def agent_step(self, reward, observation):
        return Action()

    def agent_end(self, reward):
        pass

    def agent_cleanup(self):
        pass

    def agent_message(self, inMessage):
        if inMessage is None:
            return "null"

        if inMessage == "":
            return "empty"

        if inMessage == "null":
            return None

        if inMessage == "empty":
            return ""

        return inMessage;


if __name__ == "__main__":
    AgentLoader.load_agent(TestMessageAgent())
