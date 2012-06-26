#!/usr/bin/python

import os
import sys
import logging

from stackutil.novacommand import NovaCommand

class Main(NovaCommand):
    '''Delete volumes from the Nova database.
    
    This command will list (or delete, with ``--purge``) volumes in states
    other than ``in-use`` or ``available``.  If you pass the ``--all`` flag
    it will operate on all volumes in the database.'''

    def take_action(self, args):
        NovaCommand.init_engine(self, args)

        if args.all:
            res = self.engine.execute('''
                select id,status,display_name from volumes''')
        else:
            res = self.engine.execute('''
                select id,status,display_name from volumes
                    where status not in ("in-use", "available")
                        and deleted_as is null''')

        rows = res.fetchall()

        if args.mode == 'purge':
            for id, status, name in rows:
                res = self.engine.execute(
                        'delete from volumes where id = %s', id)
                self.log.info('deleted volume %s (id %s).' % (name, id))

        return(['id', 'status', 'display name'], rows)

