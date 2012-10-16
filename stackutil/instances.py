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

    def get_parser (self, *args, **kwargs):
        p = super(Main, self).get_parser(*args, **kwargs)

        p.add_argument('--deleting', action='store_const',
                const='deleting', dest='state')
        p.add_argument('--building', action='store_const',
                const='build', dest='state')
        p.add_argument('--stuck', action='store_const',
                const='stuck', dest='state')
        p.add_argument('--reset', action='store_const',
                const='reset', dest='mode')

        return p

    def take_action(self, args):
        NovaCommand.init_engine(self, args)

        sql = '''select id, hex(id), uuid, user_id, hostname, host, vm_state, task_state
                    from instances'''

        if args.state == 'deleting':
            where_sql = 'task_state="deleting"'
        elif args.state == 'stuck':
            where_sql = 'vm_state not in ("active", "deleted")'
        elif args.state == 'building':
            where_sql = 'vm_state = "build"'

        res = self.engine.execute(' where '.join([sql, where_sql]))
        rows = res.fetchall()

        if args.mode == 'purge':
            for id, hexid, uuid, user_id, hostname, host, vm_state, task_state in rows:
                res = self.engine.execute(
                        'delete from instance_info_caches where instance_id = %s', uuid)
                res = self.engine.execute(
                        'delete from instances where id = %s', id)
                self.log.info('deleted instance %s (id %s).' % (
                    hostname, id))
        elif args.mode == 'reset':
            for id, hexid, uuid, user_id, hostname, host, vm_state, task_state in rows:
                res = self.engine.execute(
                        'update instances set vm_state="active", task_state=NULL where id = %s', id)
                self.log.info('reset instance %s (id %s).' % (
                    hostname, id))
        else:
            return([
                'id', 'uuid', 'user_id', 'hostname', 'host',
                'vm state', 'task state',
                ], (r[1:] for r in rows))

