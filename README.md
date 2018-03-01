# pybats [![Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-blue.svg?style=flat-square)](LICENSE) [![Travis](https://img.shields.io/travis/ryanvolpe/pybats.svg?style=flat-square)](https://travis-ci.org/ryanvolpe/pybats) [![Codecov](https://img.shields.io/codecov/c/github/ryanvolpe/pybats.svg?style=flat-square)](https://codecov.io/gh/ryanvolpe/pybats)


Command line utility testing inspired by [**Bats**][sstephenson/bats]<sup id='a1'>[1](#f1)</sup>.

## Usage

This readme is a brief introduction to pybats. More details may be found in the [documentation][pybats-docs].

### Pytest
Upon installation, a plugin is registered for [pytest]. This plugin provides a fixture named ``pybats`` which can be used as below:

~~~python
def test_echo(pybats):
    with pybats.command('echo', 'spam') as cmd:
        assert cmd.status == 0
        assert cmd.output == 'spam'
~~~

### Unittest, nose, *etc.*
If you're not using [pytest], pybats should still work for you. You'll just need to initialize a ``Context`` object:

~~~python
from pybats import core

def test_echo():
    pybats = core.Context()
    with pybats.command('echo', 'spam') as cmd:
        assert cmd.status == 0
        assert cmd.output == 'spam'
~~~

## Comparison with Bats

### Fixtures
Description | Bats | pybats
----------- | ---- | ------
Runs a *command* | ``run ...`` | ``with pybats.command(...) as cmd``
Command exit code | ``$status`` | ``cmd.status``
Interleaved stdout and stderr | ``$output`` | ``cmd.output``
Array of lines of output | ``${lines[@]}`` | ``cmd.lines``
Only stderr | — | ``cmd.erroutput``<sup id='a2.1'>[2](#f2)</sup>
Array of lines of stderr | — | ``cmd.errlines``<sup id='a2.2'>[2](#f2)</sup>
Set environment variable | ``VARIABLE=value`` | ``pybats.environment['VARIABLE'] = 'value'``
Load file relative to root | ``load <path>`` | —
Skip test | ``skip [message]`` | —

### Example

Let's use a few simple test cases to illustrate the differences between Bats and pybats:

- Does ``echo 'test'``:
  - print ``"test"``?
  - exit ``0``?
- Does ``util --help``:
  - print at least one line of output?
  - print a line that startswith ``"Usage:"``?
  - exit ``0``?

#### Bats

~~~bash
@test "test echo" {
    run echo 'test'
    [ "$status" -eq 0 ]
    [ "$output" = "test" ]
}

@test "command with --help option" {
    run util --help
    [ "$status" -eq 0 ]
    [ "${#lines[@]}" -ge 1 ]
    [[ "${lines[0]}" =~ Usage: ]]
}
~~~

#### pybats (using pytest fixtures)

~~~python
def test_echo(pybats):
    with pybats.command('echo', 'test') as cmd:
        assert cmd.status == 0
        assert cmd.output == 'test'

def test_command_with_help_option(pybats):
    with pybats.command('util', '--help') as cmd:
        assert cmd.status == 0
        assert len(cmd.lines) >= 1
        assert cmd.lines[0].match(r'^Usage:')
~~~

## Author's note

The original goal of this project was to run Bats tests as-written from within [pytest].

While deliberating on how to integrate the test states, the question of “why are we making people write Bash *and* Python?” presented itself, and it was decided to emulate Bats rather than adapting it directly.

---

1. [@sstephenson] is the original author of Bats, and the reference link points to the original repo accordingly. After a period of inactivity, the code was forked and development now continues at [bats-core/bats-core]. <small><a href='#a1' id='f1'>↩</a></small>
1. ``erroutput``<small>[↩](#a2.1)</small> and ``errlines``<small>[↩](#a2.2)</small> are only populated if stderr is redirected; see [the docs][pybats-docs] for details.


[@sstephenson]: https://github.com/sstephenson/
[sstephenson/bats]: https://github.com/sstephenson/bats/
[bats-core/bats-core]: https://github.com/bats-core/bats-core/
[pytest]: https://pytest.org/
[pybats-docs]: https://pybats.readthedocs.io/
