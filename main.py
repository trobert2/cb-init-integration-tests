#!/usr/bin/python

# Copyright 2013 Cloudbase Solutions Srl
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

from env_prep import env_setup
from integration_tests import check_instance

handle = env_setup.EnvironmentSetup(prepare_script='env_prep/prepare.sh',
                                    boot_script='boot_machine.sh',
                                    prepare_conf='configurations/ws12.ini')

handle.generate_boot_config(output_config='configurations/config.ini')

#handle.boot_vm(config_file='configurations/ws12.ini')

#object = check_instance.IntegrationTestsForCloudbaseInitWS12(
#    'configurations/ws12.ini', 'logs/checks.log')
#object.check_windows_server()
