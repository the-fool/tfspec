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

This code will ensure that *all* `google_compute_firewall` resources have the property `enable_logging = true`.


Forbidding a resource
---------------------

This spec will forbid the creation of `google_compute_firewall` resources

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

This spec will allow for `google_compute_firewall` to ignore the `enable_logging` key.  But if it specifies the key, it _must_ be set to the value `False`.

_Note: Without using `OPT`, all keys are assumed to be _required_ 

Requiring a key with no rule
----------------------------

To require a key, but without specifying a rule, use the `ANYTHING` validator.

.. code-block:: python

    from tfspec import Spec, ANYTHING

    spec = Spec({
        'google_compute_firewall': {
            'description': ANYTHING
        }
    })

In this case, :code:`description` must be included, but that is all we specify.  

Usually, any validator is better than `ANYTHING` -- but it is there if you need it.  A better validation would be ensuring that `description` is a string of a certain length.
