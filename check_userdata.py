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

from utils import wsutils
import logging

class UserdataTestsForCloudbaseInit(object):

    def __init__(self, config_file, log_file):
        logging.basicConfig(filename=log_file, level='DEBUG')
        self.LOG = logging.getLogger('integration tests')
        self.osutils = wsutils.WindowsServerUtilsCheck(config_file, log_file)

    def check_userdata(self):
        password = self.osutils._get_password()
        self.osutils.wait_for_boot_completion()
        if self.osutils.check_userdata_ran_correctly(password):
            self.LOG.info('extend volumes: SUCCESS\n')
        else:
            self.LOG.error('volumes not extended!\n')


handle = UserdataTestsForCloudbaseInit('configurations/config.ini',
                                       'logs/logs.log')
handle.check_userdata()