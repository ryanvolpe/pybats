# vim: fileencoding=utf-8

from pybats import core
import os
import uuid

# unit tests


def test_context_immutability():
    context = core.Context()
    try:
        context.immutable_test = False
        assert context.immutable_test
    except AttributeError:
        assert True


def test_context_environment_inherits_env():
    VARNAME = 'TEST_VAR_' + uuid.uuid4().hex.upper()
    os.environ[VARNAME] = 'test'
    context = core.Context()
    assert VARNAME in context.environment
    assert context.environment[VARNAME] == 'test'


def test_context_environment_setting():
    VARNAME = 'TEST_VAR_' + uuid.uuid4().hex.upper()
    context = core.Context()
    context.environment[VARNAME] = 'test'
    assert VARNAME in context.environment
    assert context.environment[VARNAME] == 'test'


def test_result_stdout_only():
    default = core.CommandResult(0, 'test output line #1\ntest output line #2')
    assert default.status == 0
    assert default.output == 'test output line #1\ntest output line #2'
    assert default.lines == ['test output line #1', 'test output line #2']
    assert default.erroutput is None
    assert default.errlines == []


def test_result_stdout_stderr():
    both = core.CommandResult(0, 'a\nb\n', 'x\ny\n')
    assert both.status == 0
    assert both.output == 'a\nb'
    assert both.lines == ['a', 'b']
    assert both.erroutput == 'x\ny'
    assert both.errlines == ['x', 'y']


def test_environment():
    context = core.Context()
    context.environment['ANSWER'] = '42'
    context.environment['MORE'] = 'yes'
    with context.command('echo $ANSWER $MORE', shell=True) as cmd:  # nosec
        assert cmd.status == 0
        assert cmd.output == '42 yes'
