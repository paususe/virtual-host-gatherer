# Copyright (c) 2020 SUSE LLC. All Rights Reserved.
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

"""
Contains worker interface.
"""

from __future__ import print_function, absolute_import
import logging
import json
import base64
from gatherer.modules import WorkerInterface
from collections import OrderedDict

try:
    import pynetbox
    IS_VALID = True
except ImportError:
    IS_VALID = False


class NetBox(WorkerInterface):
    """
    Worker class for NetBox.
    """

    DEFAULT_PARAMETERS = OrderedDict([
        ('hostname', ''),
        ('port', 443),
        ('private_key', ''),
        ('token', '')])

    def __init__(self):
        """
        Constructor.

        :return:
        """

        self.log = logging.getLogger(__name__)
        self.host = self.port = self.private_key = self.token = None

    # pylint: disable=R0801
    def set_node(self, node):
        """
        Set node information

        :param node: Dictionary of the node description.
        :return: void
        """

        try:
            self._validate_parameters(node)
        except AttributeError as error:
            self.log.error(error)
            raise error

        self.host = node['hostname']
        self.port = node.get('port', 443)
        self.private_key = node.get('private_key', "")
        self.token = node['token']

    def parameters(self):
        """
        Return default parameters

        :return: default parameter dictionary
        """

        return self.DEFAULT_PARAMETERS

    def run(self):
        """
        Start worker.

        :return: Dictionary of the hosts in the worker scope.
        """
        output = dict()
        self.log.info("Connect to %s:%s", self.host, self.port)

        base_url = "https://%s:%s/" % (self.host, self.port)

        try:
            nb = pynetbox.api(base_url, token=self.token, private_key=self.private_key)

            devices = nb.dcim.devices.all()
            vms = nb.virtualization.virtual_machines.all()
            tenants = nb.tenancy.tenants.all()

            for device in devices:
                self.log.debug("Device id={0}, name={1}, Type={2}".format(device.id, device.name, device.device_type))

            #for vm in vms:
            #    self.log.debug("VM={0}, role={1}, status={2}".format(vm.name, vm.role, vm.status))

            for device in devices:
                if not device.name:
                    index = format(device.id)
                else:
                    index = ''.join(format(device.name).split())

                output[index] = {
                    'type': 'netbox',
                    'name': format(device.name),
                    'hostIdentifier': format(device.id),
                    'os': format(device.platform),
                    'osVersion': format(device.platform),
                    'totalCpuSockets': 0,
                    'totalCpuCores': 0,
                    'totalCpuThreads': 0,
                    'cpuMhz': 0,
                    'cpuArch': 'cloud',
                    'ramMb': 0,
                    'vms': {},
                    'optionalVmData': {}
                }

        except Exception as exc:
            self.log.error(exc)

        return output

    def valid(self):
        """
        Check plugin class validity.

        :return: True if pyVim module is installed.
        """
        return IS_VALID
