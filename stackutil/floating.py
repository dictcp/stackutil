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
        p.add_argument('--delete', '-d', type=bool, default=False)

    def take_action(self, args):
        NovaCommand.init_engine(self, args)

        sql = 'select id,address,project_id,host from floating_ips'
        where = []
        whereargs = []

        if args.under:
            where.append('inet_aton(address) < inet_aton(%s)')
            whereargs.append(args.under)

        if args.over:
            where.append('inet_aton(address) > inet_aton(%s)')
            whereargs.append(args.over)

        if where:
            sql = '%s where %s' % (
                    sql,
                    ' AND '.join(where)
                    )

        res = self.engine.execute(sql, whereargs)
        rows = res.fetchall()

        return(['id', 'address', 'project_id', 'host'], rows)

