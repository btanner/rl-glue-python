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
import os
import network.Network as Network
from rlglue import versions
from types import Observation_action
from types import Reward_observation_action_terminal

network = None


# () -> void
def force_connection():
    global network
    if network is None:

        svn_version = versions.get_svn_codec_version()
        codec_version = versions.get_codec_version()

        host = Network.kLocalHost

        host_string = os.getenv("RLGLUE_HOST")
        port_string = os.getenv("RLGLUE_PORT")

        if host_string is not None:
            host = host_string

        try:
            port = int(port_string)
        except TypeError:
            port = Network.kDefaultPort

        print "RL-Glue Python Experiment Codec Version: " + codec_version + " (Build " + svn_version + ")"
        print "\tConnecting to " + host + " on port " + str(port) + "..."
        sys.stdout.flush()

        network = Network.Network()
        network.connect(host, port)
        network.clear_send_buffer()
        network.put_int(Network.kExperimentConnection)
        network.put_int(0)
        network.send()


# (int) -> void
def do_standard_recv(state):
    network.clear_recv_buffer()
    recv_size = network.receive(8) - 8

    glue_state = network.get_int()
    data_size = network.get_int()
    remaining = data_size - recv_size

    if remaining < 0:
        remaining = 0

    #TODO: Noticed this May 2018. This seems like a big.
    remainingReceived = network.receive(remaining)

    # Already read the header, so discard it
    network.get_int()
    network.get_int()

    if glue_state != state:
        sys.stderr.write(
            "Not synced with server. glue_state = " + str(glue_state) + " but should be " + str(state) + "\n")
        sys.exit(1)


# (int) -> void
def do_call_no_params(state):
    network.clear_send_buffer()
    network.put_int(state)
    network.put_int(0)
    network.send()


# Brian Tanner... need to make this return a string
# () -> string
def RL_init():
    force_connection()
    do_call_no_params(Network.kRLInit)
    do_standard_recv(Network.kRLInit)
    # Brian Tanner added
    taskSpecResponse = network.get_string()
    return taskSpecResponse


# () -> Observation_action
def RL_start():
    obsact = None
    do_call_no_params(Network.kRLStart)
    do_standard_recv(Network.kRLStart)
    obsact = Observation_action()
    obsact.o = network.get_observation()
    obsact.a = network.get_action()
    return obsact


# () -> Reward_observation_action_terminal
def RL_step():
    roat = None
    do_call_no_params(Network.kRLStep)
    do_standard_recv(Network.kRLStep)
    roat = Reward_observation_action_terminal()
    roat.terminal = network.get_int()
    roat.r = network.get_double()
    roat.o = network.get_observation()
    roat.a = network.get_action()
    return roat


# () -> void
def RL_cleanup():
    do_call_no_params(Network.kRLCleanup)
    do_standard_recv(Network.kRLCleanup)


# (string) -> string
def RL_agent_message(message):
    if message == None:
        message = ""
    response = ""
    force_connection()
    network.clear_send_buffer()
    network.put_int(Network.kRLAgentMessage)
    # Payload Size
    network.put_int(len(message) + 4)
    network.put_string(message)
    network.send()
    do_standard_recv(Network.kRLAgentMessage)
    response = network.get_string()
    return response


# (string) -> string
def RL_env_message(message):
    if message == None:
        message = ""
    response = ""
    force_connection()
    network.clear_send_buffer()
    network.put_int(Network.kRLEnvMessage)
    # Payload Size
    network.put_int(len(message) + 4)
    network.put_string(message)
    network.send()
    do_standard_recv(Network.kRLEnvMessage)
    response = network.get_string()
    return response


# () -> double
def RL_return():
    do_call_no_params(Network.kRLReturn)
    do_standard_recv(Network.kRLReturn)
    reward = network.get_double()
    return reward


# () -> int
def RL_num_steps():
    do_call_no_params(Network.kRLNumSteps)
    do_standard_recv(Network.kRLNumSteps)
    num_steps = network.get_int()
    return num_steps


# () -> int
def RL_num_episodes():
    do_call_no_params(Network.kRLNumEpisodes)
    do_standard_recv(Network.kRLNumEpisodes)
    num_episodes = network.get_int()
    return num_episodes


# Brian Tanner needs to make this return an int
# (int) -> int
def RL_episode(num_steps):
    network.clear_send_buffer()
    network.put_int(Network.kRLEpisode)
    network.put_int(Network.kIntSize)
    network.put_int(num_steps)
    network.send()
    do_standard_recv(Network.kRLEpisode)
    # Brian Tanner added
    exitStatus = network.get_int()
    return exitStatus
