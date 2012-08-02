#!/usr/bin/python

import os
import sys
import logging

from stackutil.novacommand import NovaCommand

class Main(NovaCommand):
    '''Clear ip addresses in the Nova database.
    
    This command will list (or deallocate, with ``--purge``) fixed
    addresses in the Nova database that are unallocated but are still
    associated with an instance id.  With the ``--all`` flag this will
    operate on all fixed addresses.'''

    def get_parser (self, *args, **kwargs):
        p = super(Main, self).get_parser(*args, **kwargs)

        p.add_argument('--under')
        p.add_argument('--over')
        p.add_argument('--unassigned', action='store_true', default=False)

        return p

    def take_action(self, args):
        NovaCommand.init_engine(self, args)

        sql = 'select id,address,project_id,host from floating_ips'
        where = []
        whereargs = []

        if not args.all:
            if args.under:
                where.append('inet_aton(address) < inet_aton(%s)')
                whereargs.append(args.under)

            if args.over:
                where.append('inet_aton(address) > inet_aton(%s)')
                whereargs.append(args.over)

            if args.unassigned:
                where.append('project_id is NULL')

        if where:
            sql = '%s where %s' % (
                    sql,
                    ' AND '.join(where)
                    )

        res = self.engine.execute(sql, whereargs)
        rows = res.fetchall()

        if args.mode == 'purge':
            for id, address, project_id, host in rows:
                res = self.engine.execute(
                        'delete from floating_ips where id = %s', id)
                self.log.info('deleted address %s (id %s).' % (address, id))

        return(['id', 'address', 'project_id', 'host'], rows)

