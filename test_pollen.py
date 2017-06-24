from pytest import raises

from pollen import Pollen, OverwriteServiceError, \
    UndefinedServiceNameError, ConfigurableServiceError


class Foo(object):
    def __init__(self, bar=0):
        self.bar = bar


def factory(container):
    return Foo()


def configurable_factory(container, bar):
    return Foo(bar)


class PollenTestCase(object):
    def setup_method(self):
        self.container = Pollen()


class TestContainer(PollenTestCase):
    def test_register_value(self):
        self.container.register('foo', [])
        assert self.container.has('foo') is True

    def test_raise_exception_when_registering_existing_name(self):
        self.container.register('foo', [])

        with raises(OverwriteServiceError) as e:
            self.container.register('foo', {})

        msg = 'Name "%s" is already in use'
        assert str(e.value) == msg % 'foo'

    def test_raise_exception_when_value_is_not_defined(self):
        with raises(UndefinedServiceNameError) as e:
            self.container.get('foo')

        msg = 'Unable to resolve "%s"'
        assert str(e.value) == msg % 'foo'

    def test_value_is_returned_by_reference(self):
        self.container.register('foo', [])
        self.container.get('foo').append(1)
        assert self.container.get('foo') == [1]

    def test_register_factory(self):
        self.container.register('foo', factory)
        assert self.container.has('foo') is True

    def test_raise_exception_when_service_is_not_defined(self):
        with raises(UndefinedServiceNameError) as e:
            self.container.get('foo')

        msg = 'Unable to resolve "%s"'
        assert str(e.value) == msg % 'foo'

    def test_factory_returns_instance(self):
        self.container.register('foo', factory)
        assert isinstance(self.container.get('foo'), Foo)

    def test_factory_always_returns_new_instances(self):
        self.container.register('foo', factory)
        assert self.container.get('foo') is not self.container.get('foo')

    def test_shared_factory_returns_instance(self):
        self.container.register('foo', factory, True)
        assert isinstance(self.container.get('foo'), Foo)

    def test_shared_factory_always_returns_same_instance(self):
        self.container.register('foo', factory, True)

        assert self.container.get('foo') is self.container.get('foo')

    def test_configurable_factory_can_not_be_shared(self):
        with raises(ConfigurableServiceError) as e:
            self.container.register('foo', configurable_factory, True)

        msg = 'Configurable services can not be shared'
        assert str(e.value) == msg

    def test_configurable_factory_returns_instance(self):
        self.container.register('foo', configurable_factory)

        result = self.container.get('foo', bar='bar')
        assert isinstance(result, Foo)
        assert result.bar == 'bar'

    def test_configurable_factory_always_returns_new_instance(self):
        self.container.register('foo', configurable_factory)

        result_a = self.container.get('foo', bar='bar')
        result_b = self.container.get('foo', bar='yada')
        assert result_a is not result_b

    def test_fqfn_as_name(self):
        self.container.register(factory, 1)

        assert self.container.has('test_pollen.factory')
        assert self.container.get('test_pollen.factory') == 1

    def test_fqcn_as_name(self):
        self.container.register(Foo, 1)

        assert self.container.has('test_pollen.Foo')
        assert self.container.get('test_pollen.Foo') == 1
