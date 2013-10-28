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
#import ConfigParser

from winrm import protocol

#logging.basicConfig(filename='/etc/integration_tests.log', level='DEBUG')
#LOG = logging.getLogger('integration tests')

#CONF = ConfigParser.ConfigParser()
#CONF.read("config.ini")


class WindowsServerUtilsCheck(object):

    #def __init__(self):
    #    self.url = CONF.get('LoginConfig', 'url')
    #    self.username = CONF.get('LoginConfig', 'username')
    #    self.password = CONF.get('LoginConfig', 'password')

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

a = WindowsServerUtilsCheck()
a._run_wsman_cmd('http://192.168.1.101',  'whatever', 'Passw0rd',
                 ['ipconfig'])
