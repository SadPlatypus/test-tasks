from .test_runner import TestRunner
from stack.algorithms.tasks.task_tree_searching import tasks, find_task_with_max_priority


def task_equals(a, b):
    return (
            not 'children' in a and
            not 'children' in b and
            a['id'] == b['id'] and
            a['name'] == b['name'] and
            a['priority'] == b['priority']
    )


def test_finding_task_with_max_priority():
    runner = TestRunner('find_task_with_max_priority')

    runner.expect_exception(lambda: find_task_with_max_priority(tasks, 13))
    runner.expect_exception(lambda: find_task_with_max_priority(tasks, 2))

    runner.expect_true(lambda: find_task_with_max_priority(tasks, 12) is None)

    runner.expect_true(lambda: task_equals(find_task_with_max_priority(tasks, 0), {
        'id': 8,
        'name': 'Выполнение тестов',
        'priority': 6,
    }))
    runner.expect_true(lambda: task_equals(find_task_with_max_priority(tasks, 1), {
        'id': 3,
        'name': 'Подготовка релиза',
        'priority': 4,
    }))

    runner.expect_true(lambda: find_task_with_max_priority(tasks, 9)['priority'] == 3)
