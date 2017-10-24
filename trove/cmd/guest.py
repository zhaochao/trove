# Copyright 2011 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import gettext
gettext.install('trove', unicode=1)

import sys

from oslo_config import cfg as openstack_cfg
from oslo_log import log as logging
from oslo_service import service as openstack_service

from trove.common import cfg
from trove.common import debug_utils
from trove.common.i18n import _LE

CONF = cfg.CONF
# The guest_id opt definition must match the one in common/cfg.py
guest_opts = [
    openstack_cfg.StrOpt('guest_id', default=None,
                         help="ID of the Guest Instance."),
    openstack_cfg.StrOpt('tenant_id', default=None,
                         help="Tenant ID of the Guest Instance."),
    openstack_cfg.StrOpt('swift_container_allowed_origins',
                         default=None,
                         help="CORS Allowed Origins for Swift Containers.")
]
monitor_opts = [
    openstack_cfg.BoolOpt('enabled', default=True,
                          help="The power of monitoring database."),
    openstack_cfg.IntOpt('measure_interval', default=300,
                         help="Interval between two metering measures."),
    openstack_cfg.IntOpt('report_interval', default=300,
                         help="Interval between two metering reports.")
]
CONF.register_opts(guest_opts)
CONF.register_opts(monitor_opts, "eayun_monitor")


def main():
    cfg.parse_args(sys.argv)
    logging.setup(CONF, None)

    debug_utils.setup()

    from trove.guestagent import dbaas
    manager = dbaas.datastore_registry().get(CONF.datastore_manager)
    if not manager:
        msg = (_LE("Manager class not registered for datastore manager %s") %
               CONF.datastore_manager)
        raise RuntimeError(msg)

    if not CONF.guest_id:
        msg = (_LE("The guest_id parameter is not set. guest_info.conf "
               "was not injected into the guest or not read by guestagent"))
        raise RuntimeError(msg)

    # rpc module must be loaded after decision about thread monkeypatching
    # because if thread module is not monkeypatched we can't use eventlet
    # executor from oslo_messaging library.
    from trove import rpc
    rpc.init(CONF)

    from trove.common.rpc import service as rpc_service
    from trove.common.rpc import version as rpc_version
    server = rpc_service.RpcService(
        manager=manager, host=CONF.guest_id,
        rpc_api_version=rpc_version.RPC_API_VERSION)

    launcher = openstack_service.launch(CONF, server)
    launcher.wait()
