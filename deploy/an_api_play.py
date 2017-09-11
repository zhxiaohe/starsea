#!/usr/bin/python3

import logging, sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager

from ansible.playbook.task import Task
from ansible.parsing.splitter import parse_kv


class Ansible:

    def __init__(self):
        self.logger = logging.getLogger("ansible")
        return

    def play(self, target_ip, tasks):
        Options = namedtuple('Options', ['connection','module_path', 'forks', 'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])
        # initialize needed objects
        variable_manager = VariableManager()
        # TODO load vars
        loader = DataLoader()
        options = Options(
            connection='ssh',
            module_path='/etc/ansible/modules',
            forks=100,
            remote_user="root",
            private_key_file="",
            ssh_common_args=None,
            ssh_extra_args=None,
            sftp_extra_args=None,
            scp_extra_args=None,
            become=True,
            become_method="sudo",
            become_user="jingu",
            verbosity=None,
            check=False)
        passwords = dict(vault_pass='secret')

        # create inventory and pass to var manager
        inventory = Inventory(loader=loader, variable_manager=variable_manager, \
                              host_list=[ip for ip in target_ip])
        variable_manager.set_inventory(inventory)

        # create play with tasks
        task_list = []
        for task in tasks:
            # task = "sysctl: name=net.ipv4.ip_forward value=1 state=present
            module, tasks_str = task.split(':', 1)
            # parse args
            kv_args = parse_kv(tasks_str)
            # create datastructure
            task_list.append(
                dict(action=dict(module=module, args=kv_args), register='shell_out'),
            )
        print(task_list)

        play_source =  dict(
            name = "Ansible Play {}".format(target_ip),
            hosts = target_ip,
            gather_facts = 'no',
            tasks = task_list
        )
        play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

        # actually run it
        tqm = None
        try:
            tqm = TaskQueueManager(
                      inventory=inventory,
                      variable_manager=variable_manager,
                      loader=loader,
                      options=options,
                      passwords=passwords,
                      # TODO callback must be an instance of CallbackBase or the name of a callback plugin
                      stdout_callback='default',
                  )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()

        return 0, ""


if __name__== "__main__":
    #tasks = ["shell:mkdir /tmp/`date +%F%H%M`","shell:mkdir /tmp/`date +%F%H%M`pc"]
    tasks = ["shell:echo 1"]
    host_ip=['10.88.20.13','10.88.20.14']
    ansible = Ansible()
    rs,r1=ansible.play(host_ip,tasks)
