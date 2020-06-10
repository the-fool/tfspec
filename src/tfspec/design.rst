Terraform Spec Design
=====================

Terraform Spec is a lightweight tool for validating Terraform plan outputs.
It is designed for simple & declarative policy enforcement on Terraform resources.

Resources
---------

Every Terraform resource is allowed unless a rule specifies that it is forbidden.

Three Key Pillars
-----------------

For every parameter of a Terraform resource there are three possible attributes:

* Is the key **required**
* Is the key **forbidden**
* Is the value **valid**

These pillars can be collapsed down to one methed: value validation.

* Is the key **required** == Is the value non-null for key
* Is the key **forbidden** == Is the value null for the key
* Is the value **valid** == Does the value pass the validator

Example spec
------------

.. code-block:: python

    from tfspec import Spec

    spec = Spec({
        'google_compute_firewall': {
            'enable_logging': True
        }
    })
    with open('tfplan.json', 'r') as plan:
        spec.validate(plan)

This code will ensure that *all* :code:`google_compute_firewall` resources have the property :code:`enable_logging = true`.

Nested spec
-----------

Data-structures can nest.  This example shows a dictionary within a dictionary.

.. code-block:: python

    from tfspec import Spec

    spec = Spec({
        'google_compute_firewall': {
            'labels': {
                'foo': str
            }
        }
    })

This code requires that :code:`labels` have the key :code:`foo` with a value that is a string.


Forbidding a resource
---------------------

This spec will forbid the creation of :code:`google_compute_firewall` resources

.. code-block:: python

    from tfspec import Spec, FORBID

    spec = Spec({
        'google_compute_firewall': FORBID
    })

Optional keys with a rule
-------------------------

To apply a rule to a key when it is present, but allow for it to be left out, make the validator optional.

.. code-block:: python

    from tfspec import Spec, OPT

    spec = Spec({
        'google_compute_firewall': {
            'enable_logging': OPT(False)
        }
    })

This spec will allow for :code:`google_compute_firewall` to ignore the :code:`enable_logging` key.  But if it specifies the key, it *must* be set to the value :code:`False`.

_Note: Without using `OPT`, all keys are assumed to be *required*. 

Requiring a key with no rule
----------------------------

To require a key, but without specifying a rule, use the :code:`ANYTHING` validator.

.. code-block:: python

    from tfspec import Spec, ANYTHING

    spec = Spec({
        'google_compute_firewall': {
            'description': ANYTHING
        }
    })

In this case, :code:`description` must be included, but that is all we specify.  

Usually, any validator is better than :code:`ANYTHING` -- but it is there if you need it.  A better validation would be ensuring that :code:`description` is a string of a certain length.

Requiring one of many rules
---------------------------

If there are many possible validators values, use :code:`ANY` to specify that *at least one* rule must pass.

.. code-block:: python

    from tfspec import Spec, Any

    spec = Spec({
        'google_kms_key_ring': {
            'location': Any('us-west1', 'us-east1)
        }
    })

Validating Lists
----------------
not sure here -- need to validate the list itself (eg, that it has length X), as well as every value in the list.

one way to do it is with a special :code:`List` datastructure that accepts a set of validators and an optional length argument.  Each member of a list must pass at least 1 of the validators.

.. code-block:: python

    from tfspec import Spec, List

    spec = Spec({
        'google_compute_firewall': {
            'allow': List([
                {
                    'protocol': 'tcp'
                },
                {
                    'protocol': 'icmp'
                }
            ], min=1)
        }
    })

This rule says that firewalls must have at least 1 :code:`allow` rule, and that they must all be for TCP or ICMP (but not, for instance, UDP).

