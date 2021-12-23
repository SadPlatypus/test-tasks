import collections

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


def find_task_with_max_priority(_tasks, group_id):
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
