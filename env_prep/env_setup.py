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

logging.basicConfig(filename='CI_creating_machine.log', level='DEBUG')
LOG = logging.getLogger('integration tests')

CONF = ConfigParser.ConfigParser()

class EnvironmentSetup(object):

    def __init__(self, prepare_script, prepare_conf, boot_script):

        self.prepare_script = prepare_script
        self.prepare_conf = prepare_conf
        self.boot_script = boot_script

    def execute_process(self, args, shell=True):
        p = subprocess.Popen(args,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=shell)
        (out, err) = p.communicate()
        return (out, err, p.returncode)

    def generate_boot_config(self, output_config):
        LOG.info('pre_boot_config')
        args = ['bash', self.prepare_script, self.prepare_conf, output_config]
        shell = False
        try:
            (out, err, ret_val) = self.execute_process(args, shell)
            LOG.info('Generate boot config ended with return code: %d'
                     % ret_val)
            LOG.debug('Generate boot config stdout:\n%s' % out)
            LOG.debug('Generate boot config stderr:\n%s' % err)
        except Exception, ex:
            LOG.error('An error occurred during'
                      ' Generate boot config execution: \'%s\'' % ex)

    def boot_vm(self, config_file, userdata = None):
        LOG.info('Booting up machine!')
        CONF.read(config_file)
        flavor_id = CONF.get('BaseVmConf', 'flavor_id')
        self.image_id = CONF.get('BaseVmConf', 'image_id')
        self.floatingip_id = CONF.get('BaseVmConf', 'floatingip_id')
        private_network = CONF.get('BaseVmConf', 'private_network')
        self.keypair = CONF.get('VmConfig', 'keypair')
        self.vm_ip = CONF.get('VmConfig', 'ip')

        args = ['bash', self.boot_script, self.output_config, flavor_id,
                self.image_id, self.keypair, private_network,
                self.floatingip_id, 'WINDOWS', userdata]
        shell = False

        try:
            (out, err, ret_val) = self.execute_process(args, shell)
            LOG.info('Boot vm ended with return code: %d' % ret_val)
            LOG.debug('Boot vm stdout:\n%s' % out)
            LOG.debug('Boot vm stderr:\n%s' % err)
        except Exception, ex:
            LOG.error('An error occurred during'
                      ' Boot vm execution: \'%s\'' % ex)
