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

import logging
import ConfigParser
import subprocess
import time

from winrm import protocol

CONF = ConfigParser.ConfigParser()


class WindowsServerUtilsCheck(object):

    def __init__(self, config_file, log_file):
        CONF.read(config_file)
        self.url = \
            'http://' + str(CONF.get('CheckList', 'ip')) + ':5985/wsman'
        self.username = CONF.get('CheckList', 'username')
        self.password = CONF.get('CheckList', 'Administrator_password')

        logging.basicConfig(filename=log_file, level='DEBUG')
        self.LOG = logging.getLogger('integration tests')

    def _execute_process(self, args, shell=True):
        p = subprocess.Popen(args,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=shell)
        (out, err) = p.communicate()
        return (out, err, p.returncode)

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

    def check_hostname_set_correctly(self):
        self.LOG.info('Testing if hostname is set correctly!')
        cmd = ['powershell', '(Get-WmiObject Win32_ComputerSystem).Name']

        response = self._run_wsman_cmd(self.url, self.username, self.password,
                                       cmd)
        if response[1]:
            self.LOG.error('Cannot get information! %s' % response[1])
        else:
            return str(response[0]) == CONF.get('CheckList', 'hostname')

    def check_user_created_correctly(self):
        self.LOG.info('Testing if create user ran correctly!')
        username_to_check = CONF.get('CheckList', 'user')
        cmd = ['powershell',
               'Get-WmiObject',
               '"Win32_Account | where -Property Name -Match %s"' %
               username_to_check
        ]

        response = self._run_wsman_cmd(self.url, self.username, self.password,
                                   cmd)
        if response[1]:
            self.LOG.error('Cannot get information! %s' % response[1])
        else:
            return response[0] is not None

    def _get_password(self):
        hostname = str(CONF.get('CheckList', 'hostname'))
        keypair = str(CONF.get('CheckList', 'keypair')) + '.pem'
        process = 'nova get-password ' + hostname + ' ' + keypair
        password = self._execute_process(process)[0]
        return str(password)

    def check_user_password_set_correctly(self):
        self.LOG.info('Testing if password was set correctly!')
        cmd = ['powershell', 'Get-Date']

        user_to_check = CONF.get('CheckList', 'user')
        password_to_check = self._get_password()
        try:
            self._run_wsman_cmd(self.url, user_to_check, password_to_check,
                                cmd)
            return True
        except Exception:
            return False

    def check_volumes_extended_correctly(self):
        self.LOG.info('Testing if extend volumes ran correctly!')
        cmd = ['powershell',  '(Get-WmiObject "win32_logicaldisk | where',
                              ' -Property DeviceID -Match C:").Size']

        image_size = CONF.get('CheckList', 'imageSize')

        response = self._run_wsman_cmd(self.url, self.username, self.password,
                                       cmd)
        if response[1]:
            self.LOG.error('Cannot get information! %s' % response[1])
        else:
            return int(response[0]) > int(image_size)

    def check_userdata_ran_correctly(self):
        self.LOG.info('Testing if userdata script ran correctly!')
        cmd = ['powershell', 'Test-Path ~\\Documents\\script.txt']

        response = self._run_wsman_cmd(self.url, self.username, self.password,
                                       cmd)

        if response[1]:
            self.LOG.error('Cannot get information! %s' % response[1])
        else:
            return bool(response[0])

    def check_multipart_userdata_ran_correctly(self):
        self.LOG.info('Testing if multipart userdata script ran correctly!')
        cmd = ['powershell', '(Get-Item ~\\Documents\\*.txt).length']

        response = self._run_wsman_cmd(self.url, self.username, self.password,
                                       cmd)

        if response[1]:
            self.LOG.error('Cannot get information! %s' % response[1])
        else:
            return int(response[0]) == 3

    def check_ssh_ran_correctly(self):
        self.LOG.info('Testing if ssh keys script ran correctly!')
        cmd = ['powershell', '(Get-Item ~\\.ssh\\*).length']

        user_to_check = CONF.get('CheckList', 'user')
        password_to_check = self._get_password()
        response = self._run_wsman_cmd(self.url, user_to_check,
                                       password_to_check, cmd)

        if response[1]:
            self.LOG.error('Cannot get information! %s' % response[1])
        else:
            return int(response[0]) > 0

    def wait_for_boot_completion(self):
        key = 'HKLM:SOFTWARE\\Wow6432Node\\Cloudbase` ' \
              'Solutions\\Cloudbase-init\\Plugins'
        cmd = ['powershell',
               '(Get-Item %s).ValueCount' % key]
        while True:
            try:
                state = self._run_wsman_cmd(self.url, self.username,
                                                self.password, cmd)
                print state[1]
                print state[0]
                if state[1]:
                    time.sleep(1)
                elif int(state[0]) == 7:
                    break

                self.LOG.debug('Waiting for plugins to run completion!')
            finally:
                pass

    #def _check_netadapter_set_correctly(self):
    #    self.LOG.info('Testing if the network adapter was set correctly!')
    #    cmd = ['powershell', 'Get-NetAdapter']
    #    response = self._run_wsman_cmd(self.url, self.username, self.password,
    #                               cmd)
    #    if response[1]:
    #        self.LOG.error('Cannot get information! %s' % response[1])
    #    else:
    #        return response[0] == CONF.get('CheckList', 'netadapter')
