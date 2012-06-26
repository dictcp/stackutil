#!/usr/bin/python

import os
import sys
import logging

from cliff.formatters.table import TableFormatter

from stackutil.novacommand import NovaCommand

class PurgeVolumes(NovaCommand):
    '''Clear volumes from the Nova database.'''

    def get_parser(self, *args, **kwargs):
        p = super(PurgeVolumes, self).get_parser(*args, **kwargs)
        p.add_argument('--all', action='store_true')
        return p

    def take_action(self, args):
        super(PurgeVolumes, self).take_action(args)

        if args.all:
            res = self.engine.execute('''
                select id,status,display_name from volumes''')
        else:
            res = self.engine.execute('''
                select id,status,display_name from volumes
                    where status not in ("in-use", "available")''')

        rows = res.fetchall()
        formatter = TableFormatter()
        formatter.emit_list(['id', 'status', 'display name'], rows,
                sys.stdout, args)

        if args.dryrun:
            return

        for id, status, name in rows:
            res = self.engine.execute(
                    'delete from volumes where id = %s', id)
            self.log.info('deleted volume id %s.' % id)

class PurgeIPS(NovaCommand):
    '''Clear ip addresses from the Nova database.'''

    def get_parser(self, *args, **kwargs):
        p = super(PurgeIPS, self).get_parser(*args, **kwargs)
        p.add_argument('--all', action='store_true')
        return p

    def take_action(self, args):
        super(PurgeIPS, self).take_action(args)

        if args.all:
            res = self.engine.execute('''
                select id,address,allocated,instance_id from fixed_ips''')
        else:
            res = self.engine.execute('''
                select id,address,allocated,instance_id from fixed_ips
                    where allocated=0 and instance_id is not null''')

        rows = res.fetchall()
        formatter = TableFormatter()
        formatter.emit_list(['id', 'address', 'allocated', 'instance id'], rows,
                sys.stdout, args)

        if args.dryrun:
            return

        for id, address, allocated, instance_id in rows:
            res = self.engine.execute(
                    'update fixed_ips set allocated=0,instance_id=NULL where id = %s', id)
            self.log.info('cleared address %s (id %s).' % (address, id))

