#!/usr/bin/env python
# Copyright 2017 Red Hat, Inc.
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

import traceback
import os

import hooking

import _cluster

_PROJECT_NAME = 'ovirt'


def main():
    caps = hooking.read_json()
    _update(caps)
    hooking.write_json(caps)


def _update(caps):
    node_name = os.environ['HOSTNAME']
    cluster = _cluster.NodeNetworkCluster(node_name, _PROJECT_NAME)
    network = cluster.get_network()
    if 'Success' not in network['state']['infoStatus']:
        hooking.exit_hook(network['state']['infoStatus']['message'])
    caps['networks'] = network['state']['capabilities']['networks']
    caps['bridges'] = network['state']['capabilities']['bridges']
    caps['vlans'] = network['state']['capabilities']['vlans']
    caps['bondings'] = network['state']['capabilities']['bondings']
    caps['nics'] = network['state']['capabilities']['nics']


if __name__ == '__main__':
    try:
        main()
    except:
        hooking.exit_hook(traceback.format_exc())
