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

import sys

import rlglue.network.Network as Network


class ClientAgent(object):
    kUnknownMessage = "Unknown Message: "
    network = None
    agent = None

    # (agent) -> void
    def __init__(self, agent):
        self.agent = agent
        self.network = Network.Network()

    # () -> void
    def on_agent_init(self):
        task_spec = self.network.get_string()
        self.agent.agent_init(task_spec)
        self.network.clear_send_buffer()
        self.network.put_int(Network.kAgentInit)
        self.network.put_int(0)  # No data following this header

    # () -> void
    def on_agent_start(self):
        observation = self.network.get_observation()
        action = self.agent.agent_start(observation)
        size = self.network.size_of_action(action)
        self.network.clear_send_buffer()
        self.network.put_int(Network.kAgentStart)
        self.network.put_int(size)
        self.network.put_action(action)

    # () -> void
    def on_agent_step(self):
        reward = self.network.get_double()
        observation = self.network.get_observation()
        action = self.agent.agent_step(reward, observation)
        size = self.network.size_of_action(action)
        self.network.clear_send_buffer()
        self.network.put_int(Network.kAgentStep)
        self.network.put_int(size)
        self.network.put_action(action)

    # () -> void
    def on_agent_end(self):
        reward = self.network.get_double()
        self.agent.agent_end(reward)
        self.network.clear_send_buffer()
        self.network.put_int(Network.kAgentEnd)
        self.network.put_int(0)  # No data in this packet

    # () -> void
    def on_agent_cleanup(self):
        self.agent.agent_cleanup()
        self.network.clear_send_buffer()
        self.network.put_int(Network.kAgentCleanup)
        self.network.put_int(0)  # No data in this packet

    # () -> void
    def on_agent_message(self):
        message = self.network.get_string()
        reply = self.agent.agent_message(message)
        self.network.clear_send_buffer()
        self.network.put_int(Network.kAgentMessage)
        if reply is None:
            # Brian Tanner added payload even for empty message (IE: send that the size is 0)
            self.network.put_int(4)
            self.network.put_int(0)
        else:
            # Brian Tanner, added 4 to the payload size because we put_string sends the string AND its size
            self.network.put_int(len(reply) + 4)
            self.network.put_string(reply)

    # (string, int, int) -> void
    def connect(self, host, port, timeout):
        self.network.connect(host, port, timeout);
        self.network.clear_send_buffer()
        self.network.put_int(Network.kAgentConnection)
        self.network.put_int(0)  # No body to this packet
        self.network.send()

    # () -> void
    def close(self):
        self.network.close()

    # () -> void
    def run_agent_event_loop(self):
        agent_state = 0
        data_size = 0
        receive_size = 0
        remaining = 0

        while agent_state != Network.kRLTerm:
            self.network.clear_recv_buffer();
            receive_size = self.network.receive(8) - 8;  # We may have received the header and part of the payload
            # We need to keep track of how much of the payload was receive'd
            agent_state = self.network.get_int()
            data_size = self.network.get_int()

            remaining = data_size - receive_size;
            if (remaining < 0):
                print("Remaining was less than 0!")
                remaining = 0

            # TODO: May 2018 this is troubling
            amountReceived = self.network.receive(remaining)

            # Already read the header, discard it
            self.network.get_int()
            self.network.get_int()

            switch = {
                Network.kAgentInit: lambda self: self.on_agent_init(),
                Network.kAgentStart: lambda self: self.on_agent_start(),
                Network.kAgentStep: lambda self: self.on_agent_step(),
                Network.kAgentEnd: lambda self: self.on_agent_end(),
                Network.kAgentCleanup: lambda self: self.on_agent_cleanup(),
                Network.kAgentMessage: lambda self: self.on_agent_message()}
            if agent_state in switch:
                switch[agent_state](self)
            elif agent_state == Network.kRLTerm:
                pass
            else:
                sys.stderr.write(Network.kUnknownMessage % (str(agent_state)))
                sys.exit(1)

            self.network.send()
