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
import ConfigParser

from winrm import protocol

logging.basicConfig(filename='integration_tests.log', level='DEBUG')
LOG = logging.getLogger('integration tests')

CONF = ConfigParser.ConfigParser()
CONF.read("config.ini")


class IntegrationTestsForCloudbaseInit(object):

    def __init__(self):
        self.url = CONF.get('LoginConfig', 'url')
        self.username = CONF.get('LoginConfig', 'username')
        self.password = CONF.get('LoginConfig', 'password')

    def _run_wsman_cmd(self, url, username, password, cmd):
        protocol.Protocol.DEFAULT_TIMEOUT = "PT3600S"

        p = protocol.Protocol(endpoint=url,
                              transport='plaintext',
                              username=username,
                              password=password)

        shell_id = p.open_shell()

        command_id = p.run_command(shell_id, cmd[0], cmd[1:])
        std_out, std_err, status_code = p.get_command_output(shell_id,
                                                             command_id)
        p.cleanup_command(shell_id, command_id)
        p.close_shell(shell_id)
        return (std_out, std_err, status_code)

    def _check_service_is_running(self):
        pass

    def _check_hostname_set_correctly(self):
        LOG.info('Testing if hostname is set correctly!')
        hostname_to_check = CONF.get('CheckList', 'hostname')
        cmd = ['powershell',
               '$a = Get-WmiObject',
               '"Win32_ComputerSystem | where -Property Name -Match %s";' %
               hostname_to_check,
               '$a']

        response = self._run_wsman_cmd(self.url, self.username, self.password,
                                       cmd)
        if response[1]:
            LOG.error('Cannot get information! %s' % response[1])
        else:
            print str(response[0])
            return response[0] is not None

    def _check_user_created_correctly(self):
        LOG.info('Testing if create user ran correctly!')
        username_to_check = CONF.get('CheckList', 'user')
        cmd = ['powershell',
            'Get-WmiObject Win32_Account | where -Property Name -Match '
            '%s' % username_to_check
        ]

        response = self._run_wsman_cmd(self.url, self.username, self.password,
                                   cmd)
        if response[1]:
            LOG.error('Cannot get information! %s' % response[1])
        else:
            return response[0] == CONF.get('CheckList', 'user')

    def _check_user_password_set_correctly(self):
        LOG.info('Testing if password was set correctly!')
        cmd = ['powershell', 'Get-Date']

        #where to get the password from ?

        user_to_check = CONF.get('CheckList', 'user')
        password_to_check = CONF.get('CheckList', 'password')
        try:
            self._run_wsman_cmd(self.url, user_to_check, password_to_check,
                                cmd)
            return True
        except Exception:
            return False

    def _check_netadapter_set_correctly(self):
        LOG.info('Testing if the network adapter was set correctly!')
        cmd = ['powershell', 'Get-NetAdapter']
        response = self._run_wsman_cmd(self.url, self.username, self.password,
                                   cmd)
        if response[1]:
            LOG.error('Cannot get information! %s' % response[1])
        else:
            return response[0] == CONF.get('CheckList', 'netadapter')

    def handle_checks(self):
        start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        LOG.info('Tests started at %s \n \n' % start_time)

        if self._check_hostname_set_correctly():
            LOG.info('hostname: SUCCESS')
        else:
            LOG.error('hostname data does not match!')

        if self._check_user_created_correctly():
            LOG.info('create user: SUCCESS')
        else:
            LOG.error('user creation data does not match!')

        if self._check_user_password_set_correctly():
            LOG.info('set password: SUCCESS')
        else:
            LOG.error('password does not match!')

        if self._check_netadapter_set_correctly():
            LOG.info('network adapter set: SUCCESS')
        else:
            LOG.error('network adapter does not match!')

a = IntegrationTestsForCloudbaseInit()
a.handle_checks()
