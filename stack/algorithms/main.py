import collections
import traceback


class TestRunner(object):
    def __init__(self, name):
        self.name = name
        self.testNo = 1

    def expectTrue(self, cond):
        try:
            if cond():
                self._pass()
            else:
                self._fail()
        except Exception as e:
            self._fail(e)

    def expectFalse(self, cond):
        self.expectTrue(lambda: not cond())

    def expectException(self, block):
        try:
            block()
            self._fail()
        except:
            self._pass()

    def _fail(self, e=None):
        print(f'FAILED: Test  # {self.testNo} of {self.name}')
        self.testNo += 1
        if e is not None:
            traceback.print_tb(e.__traceback__)

    def _pass(self):
        print(f'PASSED: Test  # {self.testNo} of {self.name}')
        self.testNo += 1


def match(string, pattern) -> bool:
    if type(string) != str or type(pattern) != str:
        raise TypeError("Оба аргумента должны быть строкового типа!")
    if len(string) != len(pattern):
        return False

    pattern_char_code_range_dict = {
        'a': (ord('a'), ord('z') + 1),
        'd': (ord('0'), ord('9') + 1),
        ' ': (ord(' '), ord(' ') + 1),
        '*': (ord('0'), ord('z') + 1)
    }

    for pattern_index, pattern_char in enumerate(pattern):
        string_char_code = ord(string[pattern_index])
        if pattern_char not in pattern_char_code_range_dict.keys():
            raise ValueError("Недопустимый символ %s !" % pattern_char)

        if string_char_code not in range(pattern_char_code_range_dict.get(pattern_char)[0],
                                         pattern_char_code_range_dict.get(pattern_char)[1]):
            return False

    return True


def testMatch():
    runner = TestRunner('match')

    runner.expectFalse(lambda: match('xy', 'a'))
    runner.expectFalse(lambda: match('x', 'd'))
    runner.expectFalse(lambda: match('0', 'a'))
    runner.expectFalse(lambda: match('*', ' '))
    runner.expectFalse(lambda: match(' ', 'a'))

    runner.expectTrue(lambda: match('01 xy', 'dd aa'))
    runner.expectTrue(lambda: match('1x', '**'))

    runner.expectException(lambda: match('x', 'w'))


tasks = {
    'id': 0,
    'name': 'Все задачи',
    'children': [
        {
            'id': 1,
            'name': 'Разработка',
            'children': [
                {'id': 2, 'name': 'Планирование разработок', 'priority': 1},
                {'id': 3, 'name': 'Подготовка релиза', 'priority': 4},
                {'id': 4, 'name': 'Оптимизация', 'priority': 2},
            ],
        },
        {
            'id': 5,
            'name': 'Тестирование',
            'children': [
                {
                    'id': 6,
                    'name': 'Ручное тестирование',
                    'children': [
                        {'id': 7, 'name': 'Составление тест-планов', 'priority': 3},
                        {'id': 8, 'name': 'Выполнение тестов', 'priority': 6},
                    ],
                },
                {
                    'id': 9,
                    'name': 'Автоматическое тестирование',
                    'children': [
                        {'id': 10, 'name': 'Составление тест-планов', 'priority': 3},
                        {'id': 11, 'name': 'Написание тестов', 'priority': 3},
                    ],
                },
            ],
        },
        {'id': 12, 'name': 'Аналитика', 'children': []},
    ],
}


def findTaskHavingMaxPriorityInGroup(_tasks, group_id):
    group_queue = collections.deque([_tasks])
    task_queue = collections.deque()

    def is_group(_node) -> bool:
        if _node.get('priority') is None:
            return True

        return False

    def has_child(_node) -> bool:
        if _node.get('children') is None:
            return False

        return True

    def find_group():
        while group_queue:
            _node = group_queue.popleft()
            if has_child(_node):
                for _child in _node['children']:
                    group_queue.append(_child)

            if _node['id'] == group_id:
                if is_group(_node):
                    return _node
                else:
                    raise Exception("Не является группой!")

        raise Exception("Группа не найдена!")

    def find_task():
        max_priority = 0
        max_priority_task = {}
        while task_queue:
            _node = task_queue.popleft()
            if has_child(_node):
                for _child in _node['children']:
                    task_queue.append(_child)

            if not is_group(_node):
                if _node['priority'] > max_priority:
                    max_priority = _node['priority']
                    max_priority_task.update(_node)

        if not max_priority_task:
            return None

        return max_priority_task

    result = find_group()

    if result:
        task_queue.append(result)
        return find_task()


def taskEquals(a, b):
    return (
            not 'children' in a and
            not 'children' in b and
            a['id'] == b['id'] and
            a['name'] == b['name'] and
            a['priority'] == b['priority']
    )


def testFindTaskHavingMaxPriorityInGroup():
    runner = TestRunner('findTaskHavingMaxPriorityInGroup')

    runner.expectException(lambda: findTaskHavingMaxPriorityInGroup(tasks, 13))
    runner.expectException(lambda: findTaskHavingMaxPriorityInGroup(tasks, 2))

    runner.expectTrue(lambda: findTaskHavingMaxPriorityInGroup(tasks, 12) is None)

    runner.expectTrue(lambda: taskEquals(findTaskHavingMaxPriorityInGroup(tasks, 0), {
        'id': 8,
        'name': 'Выполнение тестов',
        'priority': 6,
    }))
    runner.expectTrue(lambda: taskEquals(findTaskHavingMaxPriorityInGroup(tasks, 1), {
        'id': 3,
        'name': 'Подготовка релиза',
        'priority': 4,
    }))

    runner.expectTrue(lambda: findTaskHavingMaxPriorityInGroup(tasks, 9)['priority'] == 3)


testMatch()
testFindTaskHavingMaxPriorityInGroup()
