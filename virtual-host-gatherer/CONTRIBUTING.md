# Writing a new virtual host manager

Virtual host managers pluggable, independent modules written in Python 3.

A VHM connects to a remote datasource (API, database, whatever) and gets a list of hosts and guests. Guests will be represented under the hosts.

To create a new VHM, you will need to create a new .py file in the `lib/gatherer/modules` directory. That new module must contain one class that inherits from `WorkerInterface`.

## VHM class

The `WorkerInterface` subclass must provide:

* DEFAULT_PARAMETERS dictionary (OrderedDict) with the names and default values for the parameters the user must provide in a configuration file (if using VHMs alone) or in Uyuni (if using VHMs in the context of Uyuni, UI is automatically created).

* Implement the `__init__` constructor

* Implement `set_node(self, node)`

* Implement `parameters(self)`

* Implement `run(self)`. This is the most important method, where you will take the values from the parameters the user entered, connect to the remote database/hypervisor/hyperscaler and process back the data (list of remote systems).

* Implement `valid(self)`

## run(self)

In the end,


## Data

Uyuni processes the following fields provided by a VHM:

* name: cannot have spaces or be empty. It's the key for the `output[]` dictionary.
* hostIdentifier: hypervisor where N guests will be running (listed in `vms`).
* totalCpuSockets
* totalCpuCores
* totalCpuThreds
* cpuArch: must be one of the values in https://github.com/uyuni-project/uyuni/blob/master/schema/spacewalk/common/data/rhnServerArch.sql
* cpuDescription
* cpuVendor
* cpuMhz
* os
* osVersion
* type
* ramMb
* vms
* optionalVmData


For more details, check https://github.com/uyuni-project/uyuni/blob/0706fa8a8019d9033c01d7b6722c4c7fd90a9501/java/code/src/com/suse/manager/gatherer/HostJson.java#L25

The lists of guest virtual machines running on the host can be provided in the `vms` key of he dictionary.

The `optionalVmData` field provides additional data, using map format, for VMs.

## More

Please check other VHMs for more information, or report issues and suggestion in the Uyuni Project GitHub:
https://github.com/uyuni-project/uyuni/
