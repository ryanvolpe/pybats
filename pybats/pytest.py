# vim: fileencoding=utf-8

from __future__ import absolute_import

from . import core
import pytest


class PytestMatchableString(core.MatchableString):
    def assert_match(self, pattern):
        msg = "could not match '{}'".format(self)
        return self.match(pattern) or pytest.fail(msg)

    def assert_search(self, pattern):
        msg = "could not search '{}'".format(self)
        return self.search(pattern) or pytest.fail(msg)


@pytest.fixture
def pybats():
    return core.Context(matchable=PytestMatchableString)
