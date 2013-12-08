# -*- coding: UTF-8 -*-
import struct
import re
from control_words import *
from zakon.settings import RTF_DEFAULT_ENCODING


class RTFParser(object):
    def __init__(self, encoding=RTF_DEFAULT_ENCODING):
        self._encoding = encoding
        self.ignorable = False
        self.is_plain = False
        self.is_bold = False
        self.uc_skip = 0        # Number of ASCII characters to skip after a unicode character.
        self.cur_skip = 0       # Number of ASCII characters left to skip
        self.stack = []         # Whether this group (and all inside it) are "ignorable".
        self.bold_text = []
        self.out = []

    def parse(self, rtf):
        pattern = self.get_pattern_from_regex()
        self.process_rtf_by_pattern(rtf, pattern)
        return self.get_parsed_text()

    def process_rtf_by_pattern(self, rtf, pattern):
        for match in pattern.finditer(rtf):
            control_word, control_word_arg, hex, char, brace, tchar = match.groups()

            if brace:
                self.work_with_braces(brace)
            elif char:
                self.work_with_chars(char)
            elif control_word:
                self.work_with_control_words_and_arguments(control_word, control_word_arg)
            elif hex:
                self.work_with_hex(hex)
            elif tchar:
                self.work_with_tchars(tchar)

            self.append_and_modify_bold_text()

    def get_parsed_text(self):
        return ''.join(self.out)

    def work_with_braces(self, brace):
        self.cur_skip = 0
        if brace == '{':
            self.stack.append((self.uc_skip, self.ignorable, self.is_bold))
        elif brace == '}':
            self.uc_skip, self.ignorable, self.is_bold = self.stack.pop()

    def work_with_chars(self, char):
        self.cur_skip = 0
        if char == '~':
            if not self.ignorable:
                space = u"\xA0"
                self.append_symbol_to_array(space)
        elif char in '{}\\':
            if not self.ignorable:
                self.append_symbol_to_array(char)
        elif char == '*':
            self.ignorable = True

    def work_with_control_words_and_arguments(self, control_word, control_word_arg):
        self.check_is_bold_control_word(control_word)
        self.check_is_plain_text_control_word(control_word)
        self.check_plain_text_begined()
        self.check_is_rtf_control_word(control_word, control_word_arg)

    def work_with_hex(self, hex):
        if self.cur_skip > 0:
            self.cur_skip -= 1
        elif not self.ignorable:
            symbol = self.byte_to_unicode_char(hex)
            self.append_symbol_to_array(symbol)

    def work_with_tchars(self, tchar):
        if self.cur_skip > 0:
            self.cur_skip -= 1
        elif not self.ignorable:
            self.append_symbol_to_array(tchar)

    def check_is_bold_control_word(self, control_word):
        if control_word in BOLD_STYLE_CONTROL_WORD:
            self.is_bold = True
            self.is_plain = False

    def check_is_plain_text_control_word(self, control_word):
        if control_word in PLAIN_STYLE_CONTROL_WORDS:
            self.is_plain = True

    def check_is_rtf_control_word(self, control_word, control_word_arg):
        if control_word in RTF_CONTROL_WORDS:
            self.ignorable = True
        elif self.ignorable:
            pass
        elif control_word in SPECIAL_CHARS:
            self.get_char_from_special_chars(control_word)
        elif control_word == 'uc':
            self.uc_skip = int(control_word_arg)
            self.cur_skip = self.uc_skip
        elif control_word == 'u':
            code = control_word_arg
            self.get_unicode_char_from_code(code)

    def check_plain_text_begined(self):
        if self.is_plain:
            self.is_bold = False

    def get_unicode_char_from_code(self, unicode_char):
        if self.cur_skip > 0:
            self.cur_skip -= 1
        else:
            self.out.append(self.parse_unicode_char_from_code(unicode_char))
        self.cur_skip = self.uc_skip

    def get_char_from_special_chars(self, control_word):
        symbol = SPECIAL_CHARS[control_word]
        self.append_symbol_to_array(symbol)

    def append_and_modify_bold_text(self):
        if not self.is_bold:
            string_with_bold_text = ''.join(self.bold_text)
            if string_with_bold_text.startswith(u"Статья"):
                self.bold_text.append("\n")
            self.out.extend(self.bold_text)
            self.bold_text = []

    def append_symbol_to_array(self, symbol):
        if self.is_bold:
            self.bold_text.append(symbol)
        else:
            self.out.append(symbol)

    def get_pattern_from_regex(self):
        pattern = re.compile(r"\\([a-z]{1,32})(-?\d{1,10})?[ ]?|\\'([0-9a-f]{2})|\\([^a-z])|([{}])|[\r\n]+|(.)", re.I)
        return pattern

    def byte_to_unicode_char(self, hex):
        byte = int(hex, 16)
        if byte > 127:
            return (struct.pack('B', byte)).decode(self._encoding)
        else:
            return chr(byte)

    def parse_unicode_char_from_code(self, code):
        code = int(code)
        if code < 0:
            code += 0x10000
        if code > 127:
            return unichr(code)
        else:
            return chr(code)