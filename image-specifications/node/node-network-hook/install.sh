#!/usr/bin/bash

set -xe

HOOKS_DIR='/usr/libexec/vdsm/hooks'

SETUP_NETWORKS_HOOKS_DIR="$HOOKS_DIR/before_network_setup"
install -m 774 10_network_setup.py $SETUP_NETWORKS_HOOKS_DIR
install -m 664 _cluster.py $SETUP_NETWORKS_HOOKS_DIR

GET_CAPABILITIES_HOOKS_DIR="$HOOKS_DIR/after_get_caps"
install -m 774 50_network_caps.py $GET_CAPABILITIES_HOOKS_DIR
install -m 664 _cluster.py $GET_CAPABILITIES_HOOKS_DIR

GET_STATISTICS_HOOKS_DIR="$HOOKS_DIR/after_get_stats"
install -m 774 50_network_stats.py $GET_STATISTICS_HOOKS_DIR
install -m 664 _cluster.py $GET_STATISTICS_HOOKS_DIR
