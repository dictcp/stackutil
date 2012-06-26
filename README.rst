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

Available subcommands
---------------------

- ``volumes`` -- list (or delete) volumes that are not ``in-use`` or ``available``.
- ``instances`` -- list (or delete) instances that are not ``active`` or ``deleted``.
- ``ips`` -- list (or free) ips that have allocated=0 but a non-null
  ``instance_id``.
- ``services`` -- list (or delete) disabled services.

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

