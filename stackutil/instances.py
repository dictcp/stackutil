#!/usr/bin/python

import os
import sys
import logging

from stackutil.novacommand import NovaCommand

class PurgeInstances(NovaCommand):
    '''Delete instances from the Nova database.'''

    def take_action(self, args):
        NovaCommand.init_engine(self, args)

        if args.all:
            res = self.engine.execute('''
                select id, user_id, hostname, vm_state, task_state
                    from instances''')
        else:
            res = self.engine.execute('''
                select id, user_id, hostname, vm_state, task_state
                    from instances
                    where vm_state != "active"''')

        rows = res.fetchall()

        if args.mode == 'purge':
            for id, user_id, hostname, vm_state, task_state in rows:
                res = self.engine.execute(
                        'delete from instance_info_caches where id = %s', id)
                res = self.engine.execute(
                        'delete from instances where id = %s', id)
                self.log.info('deleted instance %s (id %s).' % (
                    hostname, id))

        return([
            'id', 'user_id', 'hostname',
            'vm state', 'task state',
            ], rows)

