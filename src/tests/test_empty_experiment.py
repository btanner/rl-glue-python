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

tester = GlueTest("test_empty")

task_spec = RLGlue.RL_init()

for whichEpisode in range(1, 5):
    startTuple = RLGlue.RL_start()

    if whichEpisode % 2 == 0:
        tester.check_fail(len(startTuple.a.int_array) != 0)
        tester.check_fail(len(startTuple.a.double_array) != 0)
        tester.check_fail(len(startTuple.a.char_array) != 0)

        tester.check_fail(len(startTuple.o.int_array) != 0)
        tester.check_fail(len(startTuple.o.double_array) != 0)
        tester.check_fail(len(startTuple.o.char_array) != 0)
    else:
        tester.check_fail(len(startTuple.a.int_array) != 7)
        tester.check_fail(len(startTuple.a.double_array) != 3)
        tester.check_fail(len(startTuple.a.char_array) != 1)

        tester.check_fail(len(startTuple.o.int_array) != 2)
        tester.check_fail(len(startTuple.o.double_array) != 4)
        tester.check_fail(len(startTuple.o.char_array) != 5)

    for whichStep in range(0, 5):
        stepTuple = RLGlue.RL_step()
        tester.check_fail(stepTuple.terminal != 0)
        tester.check_fail(stepTuple.r != 0)

        if whichEpisode % 2 == 0:
            tester.check_fail(len(stepTuple.a.int_array) != 0)
            tester.check_fail(len(stepTuple.a.double_array) != 0)
            tester.check_fail(len(stepTuple.a.char_array) != 0)

            tester.check_fail(len(stepTuple.o.int_array) != 0)
            tester.check_fail(len(stepTuple.o.double_array) != 0)
            tester.check_fail(len(stepTuple.o.char_array) != 0)
        else:
            tester.check_fail(len(stepTuple.a.int_array) != 7)
            tester.check_fail(len(stepTuple.a.double_array) != 3)
            tester.check_fail(len(stepTuple.a.char_array) != 1)

            tester.check_fail(len(stepTuple.o.int_array) != 2)
            tester.check_fail(len(stepTuple.o.double_array) != 4)
            tester.check_fail(len(stepTuple.o.char_array) != 5)

print tester.get_summary()
sys.exit(tester.get_fail_count())
