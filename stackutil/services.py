#!/usr/bin/python

import os
import sys
import logging

from stackutil.novacommand import NovaCommand

class Main(NovaCommand):
    '''Delete services from the Nova database.'''

    def take_action(self, args):
        NovaCommand.init_engine(self, args)

        if args.all:
            res = self.engine.execute('''
                select id, host, topic, disabled from services''')
        else:
            res = self.engine.execute('''
                select id, host, topic, disabled from services
                    where disabled=1''')

        rows = res.fetchall()

        if args.mode == 'purge':
            for id, host, topic, disabled in rows:
                res = self.engine.execute(
                        'delete from services where id = %s', id)
                self.log.info('delete service %s on %s (id %s).' % (topic, host, id))

        return ([
            'id', 'host', 'topic', 'disabled',
            ], rows)

