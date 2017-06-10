# -*- coding: utf-8 -*-

class Parser(object):
    def __init__(self, input_path=None):
        self.input_path = input_path

    def set_input_path(self, input_path):
        self.input_path = input_path

    def _clean_chars(self, chars):
        return "".join(chars.split())

    def _to_value(self, chars):
        raise NotImplementedError()

    def _to_list(self, chars):
        chars = self._clean_chars(chars)
        if not chars[0] == '[' or not chars[-1] == ']':
            return [self._to_value(chars)]

        chars = chars[1:-1].split(',')
        return [self._to_value(char.strip()) for char in chars if char]

    def _to_lists(self, chars):
        chars = self._clean_chars(chars)
        if not chars[0] == '[' or not chars[-1] == ']':
            return [self._to_value(chars)]

        chars = chars[1:-1].replace('],[', '], [').split('], [')
        return [self._to_list(char) for char in chars if char]

    def parse_data_as_single_value(self):
        output = []
        if not self.input_path:
            return output

        with open(self.input_path, 'r') as input_file:
            for line in input_file:
                output.append(self._to_value(line))

        return output

    def parse_data_as_list(self):
        output = []
        if not self.input_path:
            return output

        with open(self.input_path, 'r') as input_file:
            for line in input_file:
                output.append(self._to_list(line))

        return output

    def parse_data_as_lists(self):
        output = []
        if not self.input_path:
            return output

        with open(self.input_path, 'r') as input_file:
            for line in input_file:
                output.append(self._to_lists(line))

        return output

class IntegerParser(Parser):
    def __init__(self, path):
        super(IntegerParser, self).__init__(path)

    def _to_value(self, chars):
        chars = self._clean_chars(chars)
        return int(chars.strip())

class FloatParser(Parser):
    def __init__(self, path):
        super(FloatParser, self).__init__(path)

    def _to_value(self, chars):
        chars = self._clean_chars(chars)
        return float(chars.strip())

class StringParser(Parser):
    def __init__(self, path):
        super(StringParser, self).__init__(path)

    def _clean_chars(self, chars):
        return chars.strip().replace('"', '')

    def _to_value(self, chars):
        chars = self._clean_chars(chars)
        return chars.strip()