# vim: fileencoding=utf-8

from pybats import pytest as pytest_
import pytest


@pytest.mark.xfail()
def test_pytest_matchable_string_match_fail():
    t = pytest_.PytestMatchableString('testing')
    t.assert_match('no match')


@pytest.mark.xfail()
def test_pytest_matchable_string_search_fail():
    t = pytest_.PytestMatchableString('testing')
    t.assert_search('no match')


def test_pytest_matchable_string():
    t = pytest_.PytestMatchableString('testing')
    t.assert_match(r'^test')
    t.assert_search(r'ing')


def test_pytest_pytest_fixture(pybats):
    assert type(pybats) is pytest_.core.Context
