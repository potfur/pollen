from inspect import isfunction, isclass


class PollenException(Exception):
    pass


class OverwriteServiceError(PollenException):
    pass


class UndefinedServiceNameError(PollenException):
    pass


class ConfigurableServiceError(PollenException):
    pass


class Pollen(object):
    def __init__(self):
        self.__services = dict()
        self.__instances = dict()

    def register(self, name, definition, shared=False):
        name = self.__get_fqn(name)

        if self.has(name):
            msg = 'Name "%s" is already in use'
            raise OverwriteServiceError(msg % name)

        if not self.__is_callable(definition):
            self.__instances[name] = definition
            return

        if self.__is_configurable(definition) and shared:
            msg = 'Configurable services can not be shared'
            raise ConfigurableServiceError(msg)

        self.__services[name] = (definition, shared)

    def get(self, name, **kwargs):
        name = self.__get_fqn(name)

        if name in self.__instances:
            return self.__instances[name]

        if name not in self.__services:
            msg = 'Unable to resolve "%s"'
            raise UndefinedServiceNameError(msg % name)

        definition, shared = self.__services[name]
        instance = definition(self, **kwargs)
        if shared:
            self.__instances[name] = instance

        return instance

    def has(self, name):
        name = self.__get_fqn(name)

        return name in self.__instances or name in self.__services

    def __get_fqn(self, name):
        if isfunction(name) or isclass(name):
            return '%s.%s' % (name.__module__, name.__name__)
        return str(name)

    def __is_callable(self, definition):
        return callable(definition) or hasattr(definition, '__call__')

    def __is_configurable(self, definition):
        args = self.__get_arguments(definition)
        return len(args) > 1

    def __get_arguments(self, definition):
        func = definition
        if not isfunction(definition):
            func = definition.__call__

        try:
            from inspect import signature
            sig = signature(func)
            args = [param for param in sig.parameters]
        except ImportError:
            from inspect import getargspec
            sig = getargspec(func)
            args = filter(lambda arg: arg != 'self', sig.args)

        return args
