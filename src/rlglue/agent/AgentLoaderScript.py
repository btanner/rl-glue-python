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
import AgentLoader as AgentLoader


def main():
    usage = "PYTHONPATH=<Path to RLGlue> python AgentLoaderScript <Agent>";

    env_vars = "The following environment variables are used by the agent to control its function:\n" + \
              "RLGLUE_HOST  : If set the agent will use this ip or hostname to connect to rather than " + Network.kLocalHost + "\n" + \
              "RLGLUE_PORT  : If set the agent will use this port to connect on rather than " + str(
        Network.kDefaultPort) + "\n"

    if (len(sys.argv) < 2):
        print usage
        print env_vars
        sys.exit(1)

    AgentLoader.load_agent_like_script()


main()
