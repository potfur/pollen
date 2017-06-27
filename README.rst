Pollen
******

Pollen is a small dependency injection container for Python, that standardizes
and centralizes the way objects are constructed.


Getting started
===============

Pollen is do-it-yourself dependency container, there is no auto-wiring and no
introspection involved in object construction.
Dependencies must be defined manually.

Container acts as a registry for services, factories and for settings.


Values and instances
--------------------

Container can hold simple values, like integers, strings, lists or dicts.

.. code:: python

    pollen = Pollen()
    pollen.register('foo', 123)

    assert pollen.get('foo') == 123

It can also store instances of already existing objects.

.. code:: python

    f = Foo()

    pollen = Pollen()
    pollen.register('foo', f)

    assert c.get('foo') == f

**Note** all values registered directly are treated as *shared*, this means
that every change made to such value will also change value in container.

.. code:: python

    pollen = Pollen()
    pollen.register('foo', [])
    pollen.get('foo').append(1)

    assert c.get('foo') == [1]


Factories
---------

For object construction, container uses factories.
Factory can be any callable, that accepts container instance as first argument.
When service is requested, Pollen will execute factory and return its result.

.. code:: python

    class FooDBStuff(object):
        def __init__(db):
            pass

    def foo_factory(container):
        return FooDBStuff(container.get('db'))

    class BarFactory(object):
        def __call__(container):
            return FooDBStuff(container.get('db'))

    pollen = Pollen()
    pollen.register('db', 'dsn')
    pollen.register('foo', foo_factory)
    pollen.register('bar', BarFactory())

    assert isinstance(pollen.get('foo'), FooDBStuff)
    assert isinstance(pollen.get('bar'), FooDBStuff)


Shared instances
----------------

There are cases, when only one instance of certain service is needed.
SQLAlchemy is such example, usually there is only one instance per database.

In such case, factory can be marked as *shared*. Container will call factory
as it would happen with normal service, but this time result will be memorized.
Every other call will return existing instance.


.. code:: python

    def foo_factory(container):
        return FooDBStuff(container.get('db'))

    pollen = Pollen()
    pollen.register('db', 'dsn')
    pollen.register('foo', foo_factory, True)

    assert pollen.get('foo') is pollen.get('foo')



Configurable factories
----------------------

Factories expecting more than one argument will be treated as
*configurable factories*.
There is no auto-wiring, therefore all additional arguments must be passed when
requesting such service.

Configurable services come handy when one or more dependencies can not be
retrieved from container - eg. database sessions, frameworks request
objects etc.

.. code:: python

    def conf_factory(container, session):
        return Handler(session)

    pollen = Pollen()
    pollen.register('handler', conf_factory)

    with db.session_context() as db_session:
        pollen.get('handler', session=db_session).do_stuff()

**Note** configurable factories can not be marked as shared.


Factory decorator
-----------------

The `register` method can be also used as a factory decorator to easily
register them in a container. It requires `name` argument and accepts optional
`shared` flag - just like normal usage.

.. code:: python

    pollen = Pollen()

    @pollen.register('foo')
    def foo_factory(container):
        return FooDBStuff(container.get('db'))

    @pollen.register(name='bar', shared=True)
    def bar_factory(container):
        return BarDBStuff(container.get('db'))

    assert isinstance(pollen.get('foo'), FooDBStuff)
    assert isinstance(pollen.get('bar'), BarDBStuff)
