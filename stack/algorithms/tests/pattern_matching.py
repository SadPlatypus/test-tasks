from .test_runner import TestRunner
from stack.algorithms.tasks.pattern_matching import match_pattern


def test_pattern_matching():
    runner = TestRunner('match_pattern')

    runner.expect_false(lambda: match_pattern('xy', 'a'))
    runner.expect_false(lambda: match_pattern('x', 'd'))
    runner.expect_false(lambda: match_pattern('0', 'a'))
    runner.expect_false(lambda: match_pattern('*', ' '))
    runner.expect_false(lambda: match_pattern(' ', 'a'))

    runner.expect_true(lambda: match_pattern('01 xy', 'dd aa'))
    runner.expect_true(lambda: match_pattern('1x', '**'))

    runner.expect_exception(lambda: match_pattern('x', 'w'))
