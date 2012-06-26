#!/usr/bin/python

import os
import sys
import logging

from stackutil.novacommand import NovaCommand

class Main(NovaCommand):
    '''Delete services from the Nova database.
    
    This command will list (or delete, with ``--purge``) services in the
    Nova database that are stale (i.e., have not reported within
    service_down_time seconds).  With ``--all`` it will operate
    on all services.'''

    def get_parser(self, *args, **kwargs):
        p = super(Main, self).get_parser(*args, **kwargs)
        p.add_argument('--service-downtime', '-D', type=int)
        return p

    def take_action(self, args):
        NovaCommand.init_engine(self, args)

        if args.service_downtime:
            downtime = int(args.service_downtime)
        else:
            downtime = int(self.cfg['service_down_time'])

        if args.all:
            res = self.engine.execute('''
                select id, host, topic, disabled,
                    utc_timestamp() - updated_at
                from services''')
        else:
            res = self.engine.execute('''
                select id, host, topic, disabled,
                    utc_timestamp() - updated_at
                from services
                where utc_timestamp() - updated_at > %s''', downtime)

        rows = res.fetchall()

        if args.mode == 'purge':
            for id, host, topic, disabled, delta in rows:
                res = self.engine.execute(
                        'delete from services where id = %s', id)
                self.log.info('delete service %s on %s (id %s).' % (topic, host, id))

        return ([
            'id', 'host', 'topic', 'disabled', 'last update',
            ], rows)

