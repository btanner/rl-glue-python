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

#
# The Network class is defined in here
#

import socket
import struct
import time
import StringIO

import numpy as np

from rlglue.types import Action
from rlglue.types import Observation
from rlglue.types import RL_Abstract_Type

numpy_int_type = np.dtype('int32').newbyteorder('>')
numpy_float_type = np.dtype('float64').newbyteorder('>')
numpy_char_type = 'S1'  # numpy.dtype('uint8').newbyteorder('>')


# RL-Glue needs to know what type of object is trying to connect.
kExperimentConnection = 1
kAgentConnection = 2
kEnvironmentConnection = 3

kAgentInit = 4  # agent_* start by sending one of these values
kAgentStart = 5  # to the client to let it know what type of
kAgentStep = 6  # event to respond to
kAgentEnd = 7
kAgentCleanup = 8
kAgentMessage = 10

kEnvInit = 11
kEnvStart = 12
kEnvStep = 13
kEnvCleanup = 14
kEnvMessage = 19

kRLInit = 20
kRLStart = 21
kRLStep = 22
kRLCleanup = 23
kRLReturn = 24
kRLNumSteps = 25
kRLNumEpisodes = 26
kRLEpisode = 27
kRLAgentMessage = 33
kRLEnvMessage = 34

kRLTerm = 35

kLocalHost = "127.0.0.1"
kDefaultPort = 4096
kRetryTimeout = 2

kDefaultBufferSize = 4096
kIntSize = 4
kDoubleSize = 8
kCharSize = 1

kUnknownMessage = "Unknown Message: %s\n"


class Network(object):

    def __init__(self):
        self.sock = None
        self.receive_buffer = StringIO.StringIO('')
        self.send_buffer = StringIO.StringIO('')

        if 'numpy' in globals():
            self.getAbstractType = self.get_abstract_type_numpy
        else:
            self.getAbstractType = self.get_abstract_type_list

    def connect(self, host=kLocalHost, port=kDefaultPort, retry_timeout=kRetryTimeout):
        while self.sock is None:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                self.sock.connect((host, port))
            except socket.error, msg:
                self.sock = None
                time.sleep(retry_timeout)
            else:
                break

    def close(self):
        self.sock.close()

    def send(self):
        self.sock.sendall(self.send_buffer.getvalue())

    def receive(self, size):
        s = ''
        while len(s) < size:
            s += self.sock.recv(size - len(s))
        self.receive_buffer.write(s)
        self.receive_buffer.seek(0)
        return len(s)

    def clear_send_buffer(self):
        self.send_buffer.close()
        self.send_buffer = StringIO.StringIO()

    def clear_recv_buffer(self):
        self.receive_buffer.close()
        self.receive_buffer = StringIO.StringIO()

    def flip_send_buffer(self):
        self.clear_send_buffer()

    def flip_recv_buffer(self):
        self.clear_recv_buffer()

    def get_int(self):
        s = self.receive_buffer.read(kIntSize)
        return struct.unpack("!i", s)[0]

    def get_double(self):
        s = self.receive_buffer.read(kDoubleSize)
        return struct.unpack("!d", s)[0]

    def get_string(self):
        # If you read 0 you get "" not None so that's fine
        length = self.get_int()
        return self.receive_buffer.read(length)

    def get_abstract_type_list(self):
        num_ints = self.get_int()
        num_doubles = self.get_int()
        num_chars = self.get_int()
        return_struct = RL_Abstract_Type()

        if num_ints > 0:
            s = self.receive_buffer.read(num_ints * kIntSize)
            return_struct.int_array = list(struct.unpack("!%di" % num_ints, s))
        if num_doubles > 0:
            s = self.receive_buffer.read(num_doubles * kDoubleSize)
            return_struct.double_array = list(struct.unpack("!%dd" % num_doubles, s))
        if num_chars > 0:
            s = self.receive_buffer.read(num_chars * kCharSize)
            return_struct.char_array = list(struct.unpack("!%dc" % num_chars, s))
        return return_struct

    def get_abstract_type_numpy(self):
        num_ints = self.get_int()
        num_doubles = self.get_int()
        num_chars = self.get_int()
        return_struct = RL_Abstract_Type()

        if num_ints > 0:
            s = self.receive_buffer.read(num_ints * kIntSize)
            assert kIntSize == 4
            return_struct.int_array = np.frombuffer(s, dtype=numpy_int_type, count=num_ints)
        if num_doubles > 0:
            s = self.receive_buffer.read(num_doubles * kDoubleSize)
            return_struct.double_array = np.frombuffer(s, count=num_doubles, dtype=numpy_float_type)
        if num_chars > 0:
            s = self.receive_buffer.read(num_chars * kCharSize)
            return_struct.char_array = np.frombuffer(s, count=num_chars, dtype=numpy_char_type)
        return return_struct

    def get_observation(self):
        return Observation.from_abstract_type(self.getAbstractType())

    def get_action(self):
        return Action.from_abstract_type(self.getAbstractType())

    def put_int(self, value):
        self.send_buffer.write(struct.pack("!i", value))

    def put_double(self, value):
        self.send_buffer.write(struct.pack("!d", value))

    def put_string(self, value):
        if value is None:
            value = ''
        self.put_int(len(value))
        self.send_buffer.write(value)

    def put_observation(self, obs):
        self.put_abstract_type(obs)

    def put_action(self, action):
        self.put_abstract_type(action)

    def put_abstract_type(self, the_item):
        self.put_int(len(the_item.int_array))
        self.put_int(len(the_item.double_array))
        self.put_int(len(the_item.char_array))
        if len(the_item.int_array) > 0:
            self.send_buffer.write(struct.pack("!%di" % (len(the_item.int_array)), *the_item.int_array))
        if len(the_item.double_array) > 0:
            self.send_buffer.write(struct.pack("!%dd" % (len(the_item.double_array)), *the_item.double_array))
        if len(the_item.char_array) > 0:
            self.send_buffer.write(struct.pack("!%dc" % (len(the_item.char_array)), *the_item.char_array))

    def put_reward_observation(self, reward_obs):
        self.put_int(reward_obs.terminal)
        self.put_double(reward_obs.r)
        self.put_observation(reward_obs.o)

    @staticmethod
    def size_of_abstract_type(the_item):
        size = kIntSize * 3
        int_size = 0
        double_size = 0
        char_size = 0
        if the_item is not None:
            if the_item.int_array is not None:
                int_size = kIntSize * len(the_item.int_array)
            if the_item.double_array is not None:
                double_size = kDoubleSize * len(the_item.double_array)
            if the_item.char_array is not None:
                char_size = kCharSize * len(the_item.char_array)
        return size + int_size + double_size + char_size

    @staticmethod
    def size_of_action(action):
        return Network.size_of_abstract_type(action)

    @staticmethod
    def size_of_observation(observation):
        return Network.size_of_abstract_type(observation)

    @staticmethod
    def size_of_reward_observation(reward_observation):
        return kIntSize + kDoubleSize + Network.size_of_observation(reward_observation.o)
