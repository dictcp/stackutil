stackutil
=========

Stackutil is a collection of utilities to clean up after OpenStack when
something falls over.

The current ("Essex") release of OpenStack occasionally fails in a way such
that some data ends up "stuck" in the database.  For example: instances
stuck in the ``BUILD`` state, volumes stuck in the ``attaching`` state, and
so forth.

Stackutil provides utilities to list and purge entries from the database
that would otherwise require manual manipulation.

**WARNING**: These tools directly manipulate the underlying database
tables without regards to the normal OpenStack API.  They will very likely
break your OpenStack environment.  These tools are meant primarily to help
digging yourself out of hole when you're in the early stages of playing
with OpenStack.

Available subcommands
---------------------

- ``volumes`` -- list (or delete) volumes that are not ``in-use`` or ``available``.
- ``instances`` -- list (or delete) instances that are not ``active`` or ``deleted``.
- ``ips`` -- list (or free) ips that have allocated=0 but a non-null
  ``instance_id``.
- ``services`` -- list (or delete) stale services (services that have not
  reported in ``service_down_time`` seconds).

Example usage
-------------

To list ips that have not been correctly de-allocated::

  # stackutil ips
  +-------+-------------+-----------+-------------+
  | id    | address     | allocated | instance id |
  +-------+-------------+-----------+-------------+
  | 16673 | 10.243.28.7 |         0 | 2246        |
  +-------+-------------+-----------+-------------+

To deallocate those ips::

  # stackutils ips --purge
  cleared address 10.243.28.7 (id 16673).
  +-------+-------------+-----------+-------------+
  | id    | address     | allocated | instance id |
  +-------+-------------+-----------+-------------+
  | 16673 | 10.243.28.7 |         0 | 2246        |
  +-------+-------------+-----------+-------------+

Requirements
------------

Stackutil requires:

- cliff_ -- A framework for building command-line applications.
- nova_ -- The Nova python module.

.. _cliff: https://github.com/dreamhost/cliff
.. _nova: https://github.com/openstack/nova

License
-------

Copyright (c) 2010,2011,2012, President and Trustees of Harvard University
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

- Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.

- Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.

- Neither the name of Harvard University nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 
