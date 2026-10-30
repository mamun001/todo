import pytest

from todo import TodoList


def test_add_a_task():
    todos = TodoList()
    task_id = todos.add("buy milk")
    assert task_id == 1
    assert todos.list()[0].text == "buy milk"


def test_list_shows_tasks():
    todos = TodoList()
    todos.add("buy milk")
    todos.add("walk dog")
    assert [t.text for t in todos.list()] == ["buy milk", "walk dog"]


def test_done_marks_one_complete():
    todos = TodoList()
    first = todos.add("buy milk")
    todos.add("walk dog")
    todos.done(first)
    assert [t.done for t in todos.list()] == [True, False]


def test_done_with_bad_id_gives_an_error():
    todos = TodoList()
    todos.add("buy milk")
    with pytest.raises(ValueError):
        todos.done(99)


@pytest.mark.skip(reason="printing belongs to the CLI, which doesn't exist yet")
def test_empty_list_prints_a_message():
    pass
