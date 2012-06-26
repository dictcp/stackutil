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

        if args.mode == 'purge':
            for id, address, allocated, instance_id in rows:
                res = self.engine.execute(
                        'update fixed_ips set allocated=0,instance_id=NULL where id = %s', id)
                self.log('cleared address %s (id %s).' % (address, id))

        return(['id', 'address', 'allocated', 'instance id'], rows)

