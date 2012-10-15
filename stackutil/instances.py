#!/usr/bin/python

import os
import sys
import logging

from stackutil.novacommand import NovaCommand

class Main(NovaCommand):
    '''Delete instances from the Nova database.
    
    This command will list (or delete, with ``--purge``) instances in the
    Nova database in states other than ``active`` or ``deleted``.  If you
    pass the ``--all`` flag it will operate on all instances.'''

    def take_action(self, args):
        NovaCommand.init_engine(self, args)

        if args.all:
            res = self.engine.execute('''
                select id, hex(id), user_id, hostname, host, vm_state, task_state
                    from instances''')
        else:
            res = self.engine.execute('''
                select id, hex(id), user_id, hostname, host, vm_state, task_state
                    from instances
                    where vm_state not in ("active", "deleted")''')

        rows = res.fetchall()

        if args.mode == 'purge':
            for id, hexid, user_id, hostname, host, vm_state, task_state in rows:
                res = self.engine.execute(
                        'delete from instance_info_caches where id = %s', id)
                res = self.engine.execute(
                        'delete from instances where id = %s', id)
                self.log.info('deleted instance %s (id %s).' % (
                    hostname, id))

        return([
            'id', 'user_id', 'hostname', 'host',
            'vm state', 'task state',
            ], (r[1:] for r in rows))

