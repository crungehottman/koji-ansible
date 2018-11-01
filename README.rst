koji-ansible
============

Ansible modules to manage Koji resources

koji_tag
--------

The ``koji_tag`` module can create, update, and delete tags within Koji. It can
also manage tag inheritance. 

.. code-block:: yaml

    - name: Create a koji tag for the ceph product
      koji_tag:
        koji: mykoji
        name: ceph-3.2-rhel-7
        state: present

Python paths
------------

These modules import from other files in the ``library`` directory. If you get
``ImportError`` when using these modules,  set the ``PYTHONPATH`` environment
variable to this ``library`` directory.

For example, if you have a ``koji.yml`` playbook that you run with
``ansible-playbook``, it should live alongside this ``library`` directory::

    top
    ├── koji.yml
    └── library

and you should run the playbook like so::

   PYTHONPATH=library ansible-playbook koji.yml


TODO
----

* Ansible-compatible docs
* Unit tests
* ``koji_target`` module to manage build targets
* Content generator configuration (user management?)
* Support ``KOJI_PROFILE`` env var instead of having to hardcode a ``koji``
  parameter on each play, similar to how the `OpenStack modules
  <https://docs.ansible.com/ansible/latest/modules/os_server_module.html>`_ can
  use the ``OS_USERNAME`` env var.
* A lower-level ``koji_call`` module to make arbitrary RPCs? Like

  .. code-block:: yaml

      koji_call:
        profile: brew
        name: createTag
        args:
          name: ceph-3.2-rhel-7
          parent: ...
        failable: true

  This is going to fail a lot of the time (eg createTag for a tag name that
  already exists).

* The long-term goal of this project is to merge into `ansible
  <https://github.com/ansible/ansible/tree/devel/lib/ansible/modules>`_ itself
  so that the modules are built in. To that end, this koji-ansible project is
  licensed under the GPLv3 to match Ansible's license.