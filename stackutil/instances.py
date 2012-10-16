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
        p.add_argument('--building', '--build', action='store_const',
                const='build', dest='state')
        p.add_argument('--stuck', action='store_const',
                const='stuck', dest='state')
        p.add_argument('--uuid')
        p.add_argument('--reset', action='store_const',
                const='reset', dest='mode')

        return p

    def take_action(self, args):
        NovaCommand.init_engine(self, args)

        sql = '''select id, hex(id), uuid, user_id, hostname, host, vm_state, task_state
                    from instances'''
        where_sql = []
        where_args = []

        if args.state == 'deleting':
            where_sql.append('task_state="deleting"')
        elif args.state == 'stuck':
            where_sql.append('vm_state not in ("active", "deleted")')
        elif args.state == 'build':
            where_sql.append('vm_state = "build"')
        
        if args.id:
            where_sql.append('id = %s')
            where_args.append(args.id)

        if args.uuid:
            where_sql.append('uuid = %s')
            where_args.append(args.uuid)

        if where_sql:
            sql = '%s where %s' % (sql, ' and '.join(where_sql))

        res = self.engine.execute(sql, where_args)
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

