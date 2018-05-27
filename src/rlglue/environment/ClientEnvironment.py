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

import sys

import rlglue.network.Network as Network


class ClientEnvironment(object):
    kUnknownMessage = "Unknown Message: "
    network = None
    env = None

    # (agent) -> void
    def __init__(self, environment):
        self.env = environment
        self.network = Network.Network()

    # () -> void
    def on_env_init(self):
        taskSpec = self.env.env_init()
        self.network.clear_send_buffer()
        self.network.put_int(Network.kEnvInit)
        self.network.put_int(len(taskSpec) + 4)  # Also including the length put in by put_string
        self.network.put_string(taskSpec)

    # () -> void
    def on_env_start(self):
        observation = self.env.env_start()
        size = self.network.size_of_observation(observation)
        self.network.clear_send_buffer()
        self.network.put_int(Network.kEnvStart)
        self.network.put_int(size)
        self.network.put_observation(observation)

    # () -> void
    def on_env_step(self):
        action = self.network.get_action()
        reward_observation = self.env.env_step(action)
        size = self.network.size_of_reward_observation(reward_observation)
        self.network.clear_send_buffer()
        self.network.put_int(Network.kEnvStep)
        self.network.put_int(size)
        self.network.put_reward_observation(reward_observation)

    # () -> void
    def on_env_cleanup(self):
        self.env.env_cleanup()
        self.network.clear_send_buffer()
        self.network.put_int(Network.kEnvCleanup)
        self.network.put_int(0)  # No data in this packet

    # () -> void
    def on_env_message(self):
        message = self.network.get_string()
        reply = self.env.env_message(message)
        self.network.clear_send_buffer()
        self.network.put_int(Network.kEnvMessage)
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
        self.network.connect(host, port, timeout)
        self.network.clear_send_buffer()
        self.network.put_int(Network.kEnvironmentConnection)
        self.network.put_int(0)  # No body to this packet
        self.network.send()

    # () -> void
    def close(self):
        self.network.close()

    # () -> void
    def run_environment_event_loop(self):
        env_state = 0
        data_size = 0
        receive_size = 0
        remaining = 0

        while env_state != Network.kRLTerm:
            self.network.clear_recv_buffer();
            receive_size = self.network.receive(8) - 8  # We may have received the header and part of the payload
            # We need to keep track of how much of the payload was receive'd
            env_state = self.network.get_int()
            data_size = self.network.get_int()

            remaining = data_size - receive_size
            if remaining < 0:
                print("Remaining was less than 0!")
                remaining = 0

            # TODO: May 2018 - this is worrisome that this is not used
            amount_received = self.network.receive(remaining)

            # Already read the header, discard it
            self.network.get_int()
            self.network.get_int()

            switch = {
                Network.kEnvInit: lambda this: this.on_env_init(),
                Network.kEnvStart: lambda this: this.on_env_start(),
                Network.kEnvStep: lambda this: this.on_env_step(),
                Network.kEnvCleanup: lambda this: this.on_env_cleanup(),
                Network.kEnvMessage: lambda this: this.on_env_message()}
            if env_state in switch:
                switch[env_state](self)
            elif env_state == Network.kRLTerm:
                pass
            else:
                sys.stderr.write(Network.kUnknownMessage % (str(env_state)))
                sys.exit(1)

            self.network.send()
