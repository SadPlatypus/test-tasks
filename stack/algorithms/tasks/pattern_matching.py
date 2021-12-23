def match_pattern(string, pattern) -> bool:
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
