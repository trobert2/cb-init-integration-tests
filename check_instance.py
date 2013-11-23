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

import datetime
import logging
from utils import wsutils

class IntegrationTestsForCloudbaseInit(object):

    def __init__(self, config_file, log_file):
        logging.basicConfig(filename=log_file, level='DEBUG')
        self.LOG = logging.getLogger('integration tests')
        self.osutils = wsutils.WindowsServerUtilsCheck(config_file, log_file)

    def check_windows_server(self):
        self.osutils.wait_for_boot_completion()
        start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.LOG.info('Tests started at %s \n \n' % start_time)

        if self.osutils.check_hostname_set_correctly():
            self.LOG.info('hostname: SUCCESS\n')
        else:
            self.LOG.error('hostname data does not match!\n')

        if self.osutils.check_user_created_correctly():
            self.LOG.info('create user: SUCCESS\n')
        else:
            self.LOG.error('user creation data does not match!\n')

        if self.osutils.check_user_password_set_correctly():
            self.LOG.info('set password: SUCCESS\n')
        else:
            self.LOG.error('password does not match!\n')

        if self.osutils.check_volumes_extended_correctly():
            self.LOG.info('extend volumes: SUCCESS\n')
        else:
            self.LOG.error('volumes not extended!\n')

        if self.osutils.check_multipart_userdata_ran_correctly():
            self.LOG.info('multipart userdata scripts: SUCCESS\n')
        else:
            self.LOG.error('multipart userdata scripts fail!\n')

        if self.osutils.check_ssh_ran_correctly():
            self.LOG.info('set ssh keys: SUCCESS\n')
        else:
            self.LOG.error('set ssh keys plugin failed!\n')

        #if self._check_netadapter_set_correctly():
        #    self.LOG.info('network adapter set: SUCCESS\n')
        #else:
        #    self.LOG.error('network adapter does not match!\n')

handle = IntegrationTestsForCloudbaseInit('configurations/config.ini',
                                          'logs/logs.log')
handle.check_windows_server()

#handle = wsutils.WindowsServerUtilsCheck('configurations/config.ini',
#                                         'logs/logs.log')

