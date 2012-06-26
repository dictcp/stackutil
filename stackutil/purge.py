#!/usr/bin/python

import os
import sys
import logging

from stackutil.novacommand import NovaCommand

class PurgeVolumes(NovaCommand):
    '''Clear volumes from the Nova database.'''

    def get_parser(self, *args, **kwargs):
        p = super(PurgeVolumes, self).get_parser(*args, **kwargs)
        p.add_argument('--all', action='store_true')
        return p

    def take_action(self, args):
        NovaCommand.init_engine(self, args)

        if args.all:
            res = self.engine.execute('''
                select id,status,display_name from volumes''')
        else:
            res = self.engine.execute('''
                select id,status,display_name from volumes
                    where status not in ("in-use", "available")''')

        rows = res.fetchall()

        if not args.dryrun:
            for id, status, name in rows:
                res = self.engine.execute(
                        'delete from volumes where id = %s', id)

        return(['id', 'status', 'display name'], rows)

class PurgeIPS(NovaCommand):
    '''Clear ip addresses from the Nova database.'''

    def get_parser(self, *args, **kwargs):
        p = super(PurgeIPS, self).get_parser(*args, **kwargs)
        p.add_argument('--all', action='store_true')
        return p

    def take_action(self, args):
        NovaCommand.init_engine(self, args)

        if args.all:
            res = self.engine.execute('''
                select id,address,allocated,instance_id from fixed_ips''')
        else:
            res = self.engine.execute('''
                select id,address,allocated,instance_id from fixed_ips
                    where allocated=0 and instance_id is not null''')

        rows = res.fetchall()

        if not args.dryrun:
            for id, address, allocated, instance_id in rows:
                res = self.engine.execute(
                        'update fixed_ips set allocated=0,instance_id=NULL where id = %s', id)

        return(['id', 'address', 'allocated', 'instance id'], rows)

class PurgeInstances(NovaCommand):
    '''Delete instances from the Nova database.'''

    def get_parser(self, *args, **kwargs):
        p = super(PurgeInstances, self).get_parser(*args, **kwargs)
        p.add_argument('--all', action='store_true')
        return p

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

        if not args.dryrun:
            for id, user_id, hostname, vm_state, task_state in rows:
                res = self.engine.execute(
                        'delete from instance_info_caches where id = %s', id)
                res = self.engine.execute(
                        'delete from instances where id = %s', id)

        return([
            'id', 'user_id', 'hostname',
            'vm state', 'task state',
            ], rows)

class PurgeServices(NovaCommand):
    '''Delete services from the Nova database.'''

    def get_parser(self, *args, **kwargs):
        p = super(PurgeServices, self).get_parser(*args, **kwargs)
        p.add_argument('--all', action='store_true')
        return p

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

        if not args.dryrun:
            for id, host, topic, disabled in rows:
                res = self.engine.execute(
                        'delete from services where id = %s', id)

                self.log.info('delete service %s on %s (id %s).' % (topic, host, id))

        return ([
            'id', 'host', 'topic', 'disabled',
            ], rows)

