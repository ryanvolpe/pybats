# pybats: simple command line tests
[![Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-blue.svg?style=flat-square)](LICENSE) [![Travis](https://img.shields.io/travis/ryanvolpe/pybats.svg?style=flat-square)](https://travis-ci.org/ryanvolpe/pybats) [![Codecov](https://img.shields.io/codecov/c/github/ryanvolpe/pybats.svg?style=flat-square)](https://codecov.io/gh/ryanvolpe/pybats)

###### **–»** Utility testing, inspired by [**Bats**][sstephenson/bats].<sup id='a1'>[\[1\]](#f1)</sup>

---

**Note** This readme is intended as a brief introduction, and assumes [pytest] as the test framework. Instructions to support other test frameworks are in the [documentation][pybats-docs].

## Example

**Command under test, and expected output:**
<pre>
<b>$ democli --xxx-unknown-option</b>
Error: unknown option --xxx-unknown-option
Usage: democli [OPTIONS] <command>
</pre>

**Using ``pybats``:**

~~~python
def test_cli_unknown_option(pybats):
    with pybats.command('democli', '--xxx-unknown-option') as cmd:
        # ensure exit code was NOT 0
        assert cmd.status != 0
        # check that the first line of output is an error message
        cmd.lines[0].assert_match(r'(?i)Error: unknown option')
        # check that the error message includes the unknown option
        cmd.lines[0].assert_search(r'\b---xxx-unknown-option\b')
        # check that the last line of output is usage information
        cmd.lines[-1].assert_match(r'(?i)^Usage: democli')
~~~

**Without ``pybats``:**

~~~python
import re
import subprocess

def test_cli_unknown_option():
    proc = subprocess.Popen(
        ['democli', '--xxx-unknown-option'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True)
    stdout, stderr = proc.communicate()
    # ensure exit code was NOT 0
    assert proc.returncode != 0
    # check that the first line of output is an error message
    lines = stdout.split('\n')
    assert re.match(r'(?i)Error: unknown option', lines[0])
    # check that the error message includes the unknown option
    assert re.search(r'\b--xxx-unknown-option\b', lines[0])
    # check that the last line of output is usage information
    assert re.match(r'(?i)Usage: democli', lines[-1])
~~~

## Alternatives

<dl>
    <dt><a href='https://bitheap.org/cram'>cram</a></dt>
    <dd>
        <blockquote>a functional testing framework for command line applications based on Mercurial's unified test format</blockquote>
        Worth taking a look at, especially for writing tests in a declarative style.
    </dd>
</dl>

## Author's note

The original goal of this project was to run Bats tests as-written from within [pytest].

While deliberating on how to integrate the test states, the question of “why are we making people write Bash *and* Python?” presented itself, and it was decided to emulate Bats rather than adapting it directly.

---

1. [@sstephenson] is the original author of Bats, and the reference link points to the original repo accordingly. After a period of inactivity, the code was forked and development now continues at [bats-core/bats-core]. <small><a href='#a1' id='f1'>↩</a></small>


[@sstephenson]: https://github.com/sstephenson/
[sstephenson/bats]: https://github.com/sstephenson/bats/
[bats-core/bats-core]: https://github.com/bats-core/bats-core/
[pytest]: https://pytest.org/
[pybats-docs]: https://pybats.readthedocs.io/
