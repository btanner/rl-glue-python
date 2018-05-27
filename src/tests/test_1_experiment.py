# 
# Copyright (C) 2008, Brian Tanner
# 
# http://rl-glue-ext.googlecode.com/
#
# Licensed under the Apache License, Version 2.0 (the "License")
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

import sys

import rlglue.RLGlue as RLGlue
from gluetest import GlueTest

tester = GlueTest("test_1")

task_spec = RLGlue.RL_init()

RLGlue.RL_start()

roat = RLGlue.RL_step()
tester.check_fail("one|1.|one" != RLGlue.RL_env_message("one"))
tester.check_fail("one|1.|one" != RLGlue.RL_agent_message("one"))
tester.check_fail(roat.terminal != 0)
tester.check_fail(roat.r != 1.0)
tester.check_fail(len(roat.o.int_array) != 1)
tester.check_fail(len(roat.o.double_array) != 0)
tester.check_fail(len(roat.o.char_array) != 0)
tester.check_fail(roat.o.int_array[0] != 0)

roat = RLGlue.RL_step()
tester.check_fail("two|2.2.|two" != RLGlue.RL_env_message("two"))
tester.check_fail("two|2.2.|two" != RLGlue.RL_agent_message("two"))
tester.check_fail(roat.terminal != 0)
tester.check_fail(roat.r != 1.0)
tester.check_fail(len(roat.o.int_array) != 1)
tester.check_fail(len(roat.o.double_array) != 0)
tester.check_fail(len(roat.o.char_array) != 0)
tester.check_fail(roat.o.int_array[0] != 1)

roat = RLGlue.RL_step()
tester.check_fail("three||three" != RLGlue.RL_env_message("three"))
tester.check_fail("three||three" != RLGlue.RL_agent_message("three"))
tester.check_fail(roat.terminal != 0)
tester.check_fail(roat.r != 1.0)
tester.check_fail(len(roat.o.int_array) != 1)
tester.check_fail(len(roat.o.double_array) != 0)
tester.check_fail(len(roat.o.char_array) != 0)
tester.check_fail(roat.o.int_array[0] != 2)

roat = RLGlue.RL_step()
tester.check_fail("four|4.|four" != RLGlue.RL_env_message("four"))
tester.check_fail("four|4.|four" != RLGlue.RL_agent_message("four"))
tester.check_fail(roat.terminal != 0)
tester.check_fail(roat.r != 1.0)
tester.check_fail(len(roat.o.int_array) != 1)
tester.check_fail(len(roat.o.double_array) != 0)
tester.check_fail(len(roat.o.char_array) != 0)
tester.check_fail(roat.o.int_array[0] != 3)

roat = RLGlue.RL_step()
tester.check_fail("five|5.5.|five" != RLGlue.RL_env_message("five"))
tester.check_fail("five|4.|five" != RLGlue.RL_agent_message("five"))
tester.check_fail(roat.terminal == 0)
tester.check_fail(roat.r != 1.0)

roat = RLGlue.RL_step()
tester.check_fail(roat.terminal != 0)
tester.check_fail(roat.r != -2.0)
tester.check_fail(len(roat.o.int_array) != 5)
tester.check_fail(len(roat.o.double_array) != 5)
tester.check_fail(len(roat.o.char_array) != 5)
tester.check_fail(roat.o.int_array[0] != 173)
tester.check_fail(roat.o.int_array[1] != -173)
tester.check_fail(roat.o.int_array[2] != 2147483647)
tester.check_fail(roat.o.int_array[3] != 0)
tester.check_fail(roat.o.int_array[4] != -2147483648)
tester.check_fail(roat.o.double_array[0] != 0.0078125)
tester.check_fail(roat.o.double_array[1] != -0.0078125)
tester.check_fail(roat.o.double_array[2] != 0.0)
tester.check_fail(roat.o.double_array[3] != 0.0078125e150)
tester.check_fail(roat.o.double_array[4] != -0.0078125e150)
tester.check_fail(roat.o.char_array[0] != 'g')
tester.check_fail(roat.o.char_array[1] != 'F')
tester.check_fail(roat.o.char_array[2] != '?')
tester.check_fail(roat.o.char_array[3] != ' ')
tester.check_fail(roat.o.char_array[4] != '&')

print tester.get_summary()
sys.exit(tester.get_fail_count())
