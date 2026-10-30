import runpy

from hello import hello


def test_hello_returns_hello():
    assert hello() == "hello"


def test_script_prints_hello(capsys):
    runpy.run_path("hello.py", run_name="__main__")
    assert capsys.readouterr().out == "hello\n"
