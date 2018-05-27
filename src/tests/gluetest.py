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


class GlueTest(object):
    caller_name = "not set"
    fail_count = 0
    test_count = 0

    def __init__(self, caller_name):
        self.caller_name = caller_name
        self.fail_count = 0
        self.test_count = 0

    def check_fail(self, did_fail):
        self.test_count = self.test_count + 1
        if did_fail:
            self.fail_count = self.fail_count + 1
            print "Failed test " + str(self.test_count)

    def get_fail_count(self):
        return self.fail_count

    def get_summary(self):
        if self.fail_count > 0:
            return "Failed " + str(self.fail_count) + " / " + str(self.test_count) + " in " + self.caller_name;
        else:
            return "Passed all " + str(self.test_count) + " checks in " + self.caller_name;
