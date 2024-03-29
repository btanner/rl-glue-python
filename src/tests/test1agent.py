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


from rlglue.agent.Agent import Agent
from rlglue.agent import AgentLoader as AgentLoader
from rlglue.types import Action


class Test1Agent(Agent):
    stepCount = 0

    def agent_init(self, taskSpec):
        self.stepCount = 0

    def agent_start(self, observation):
        self.stepCount = 0
        action = Action()
        action.int_array = observation.int_array
        action.double_array = observation.double_array
        action.char_array = observation.char_array

        return action

    def agent_step(self, reward, observation):
        self.stepCount = self.stepCount + 1
        action = Action()
        action.int_array = observation.int_array
        action.double_array = observation.double_array
        action.char_array = observation.char_array

        return action

    def agent_end(self, reward):
        pass

    def agent_cleanup(self):
        pass

    def agent_message(self, inMessage):
        timesToPrint = self.stepCount % 3

        outMessage = inMessage + "|"
        for i in range(0, timesToPrint):
            outMessage = outMessage + "%d" % (self.stepCount)
            outMessage = outMessage + "."

        outMessage = outMessage + "|" + inMessage

        return outMessage


if __name__ == "__main__":
    AgentLoader.load_agent(Test1Agent())
