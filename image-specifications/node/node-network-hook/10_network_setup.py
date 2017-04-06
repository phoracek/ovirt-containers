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

import os
import traceback

import six

import hooking

import _cluster

_PROJECT_NAME = 'ovirt'
_SETUP_TIMEOUT = 120


def main():
    data = hooking.read_json()
    networks = data['request']['networks']
    bondings = data['request']['bondings']

    _setup(networks, bondings)

    data['request']['networks'] = {}
    data['request']['bondings'] = {}
    data['request']['options']['connectivityCheck'] = False
    hooking.write_json(data)


def _setup(networks, bondings):
    node_name = os.environ['HOSTNAME']
    cluster = _cluster.NodeNetworkCluster(node_name, _PROJECT_NAME)
    attachment = cluster.get_network()
    _apply_changes(networks, bondings, attachment)
    network_version = cluster.set_network(attachment)

    # XXX: this can be triggered by spec change, we must watch setup changes.
    for event in cluster.watch_network(_SETUP_TIMEOUT):
        if event['TYPE'] == 'MODIFIED':
            network = event['object']
            if int(network['metadata']['resourceVersion']) <= network_version:
                continue
            if 'Failed' in network['state']['setupStatus']:
                hooking.exit_hook(
                    network['state']['setupStatus']['Failed']['message'])
            return


def _apply_changes(networks, bondings, attachment):
    desired_networks = attachment['spec'].setdefault('networks', {})
    for name, attrs in six.viewitems(networks):
        if 'remove' in attrs:
            desired_networks.pop(name, None)
        else:
            desired_networks[name] = attrs

    desired_bondings = attachment['spec'].setdefault('bondings', {})
    for name, attrs in six.viewitems(bondings):
        if 'remove' in attrs:
            desired_bondings.pop(name, None)
        else:
            desired_bondings[name] = attrs


if __name__ == '__main__':
    try:
        main()
    except:
        hooking.exit_hook(traceback.format_exc())
