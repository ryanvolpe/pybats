#!/usr/bin/env python
# vim: fileencoding=utf-8

import attr
import os
import re
import six
import subprocess   # nosec


class MatchableString(six.text_type):
    def match(self, pattern):
        return re.match(pattern, self)

    def search(self, pattern):
        return re.search(pattern, self)


@attr.s(slots=True, frozen=True)
class Context(object):
    environment = attr.ib(init=False)
    matchable = attr.ib(default=MatchableString)

    @environment.default
    def environment_default(self):
        return dict(os.environ)

    def command(self, *args, **kws):
        return CommandContextManager(self, args, kws)


def _typesafe(method, *args, **kws):
    type_ = type(method.__self__)
    return type_(method(*args, **kws))


@attr.s(slots=True, frozen=True)
class CommandResult(object):
    status = attr.ib()
    output = attr.ib(converter=lambda s: _typesafe(s.rstrip, '\n'))
    lines = attr.ib(init=False)
    erroutput = attr.ib(
        default=None,
        converter=lambda s: s if not s else _typesafe(s.rstrip, '\n'))
    errlines = attr.ib(init=False)

    @lines.default
    def lines_default(self):
        type_ = type(self.output)
        return [type_(s) for s in self.output.split('\n')]

    @errlines.default
    def errlines_default(self):
        if not self.erroutput:
            return []
        else:
            conv = type(self.erroutput)
            return [conv(s) for s in self.erroutput.split('\n')]


@attr.s(slots=True, frozen=True)
class CommandContextManager(object):
    fixture = attr.ib()
    _args = attr.ib()
    _kws = attr.ib()

    def _format_popen_args(self):
        args = self._args
        kws = dict(
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        kws.update(self._kws)
        kws.update(env=self.fixture.environment)
        kws.update(universal_newlines=True)
        return args, kws

    def _run_subprocess(self):
        # do the thing!
        args, kws = self._format_popen_args()
        try:
            proc = subprocess.Popen(args, **kws)    # nosec
            stdout, stderr = proc.communicate()
            rc = proc.returncode
        except OSError:
            # emulate Bash "command not found"
            rc = 127
            stdout = stderr = 'pybats: {}: command not found'.format(args[0])

        return rc, stdout, stderr

    def __enter__(self):
        rc, stdout, stderr = self._run_subprocess()
        matchable = self.fixture.matchable
        output = matchable(stdout.rstrip('\n'))
        error = matchable(stderr.rstrip('\n')) if stderr is not None else None
        return CommandResult(rc, output, error)

    def __exit__(self, exc_cls, exc_val, exc_tb):
        return
