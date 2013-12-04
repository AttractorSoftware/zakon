# -*- coding: UTF-8 -*-
import struct
import re
from zakon.settings import RTF_DEFAULT_ENCODING

SPECIAL_CHARS = {'par': '\n', 'sect': '\n\n', 'page': '\n\n', 'line': '\n', 'tab': '\t', 'emdash': u'\u2014',
                 'endash': u'\u2013',
                 'emspace': u'\u2003', 'enspace': u'\u2002', 'qmspace': u'\u2005', 'bullet': u'\u2022',
                 'lquote': u'\u2018',
                 'rquote': u'\u2019', 'ldblquote': u'\201C', 'rdblquote': u'\u201D', }

RTF_CONTROL_WORDS = frozenset((
    'aftncn', 'aftnsep', 'aftnsepc', 'annotation', 'atnauthor', 'atndate', 'atnicn', 'atnid', 'atnparent', 'atnref',
    'atntime', 'atrfend', 'atrfstart', 'author', 'background', 'bkmkend', 'bkmkstart', 'blipuid', 'buptim', 'category',
    'colorschememapping', 'colortbl', 'comment', 'company', 'creatim', 'datafield', 'datastore', 'defchp', 'defpap',
    'do',
    'doccomm', 'docvar', 'dptxbxtext', 'ebcend', 'ebcstart', 'factoidname', 'falt', 'fchars', 'ffdeftext', 'ffentrymcr',
    'ffexitmcr', 'ffformat', 'ffhelptext', 'ffl', 'ffname', 'ffstattext', 'file', 'filetbl',
    'fldtype', 'fname', 'fontemb', 'fontfile', 'fonttbl', 'footer', 'footerf', 'footerl', 'footerr', 'footnote',
    'formfield', 'ftncn', 'ftnsep', 'ftnsepc', 'g', 'generator', 'gridtbl', 'header', 'headerf', 'headerl', 'headerr',
    'hl',
    'hlfr', 'hlinkbase', 'hlloc', 'hlsrc', 'hsv', 'htmltag', 'info', 'keycode', 'keywords', 'latentstyles', 'lchars',
    'levelnumbers', 'leveltext', 'lfolevel', 'linkval', 'list', 'listlevel', 'listname', 'listoverride',
    'listoverridetable', 'listpicture', 'liststylename', 'listtable', 'listtext', 'lsdlockedexcept', 'macc', 'maccPr',
    'mailmerge', 'maln', 'malnScr', 'manager', 'margPr', 'mbar', 'mbarPr', 'mbaseJc', 'mbegChr', 'mborderBox',
    'mborderBoxPr', 'mbox', 'mboxPr', 'mchr', 'mcount', 'mctrlPr', 'md', 'mdeg', 'mdegHide', 'mden', 'mdiff', 'mdPr',
    'me',
    'mendChr', 'meqArr', 'meqArrPr', 'mf', 'mfName', 'mfPr', 'mfunc', 'mfuncPr', 'mgroupChr', 'mgroupChrPr', 'mgrow',
    'mhideBot', 'mhideLeft', 'mhideRight', 'mhideTop', 'mhtmltag', 'mlim', 'mlimloc', 'mlimlow', 'mlimlowPr', 'mlimupp',
    'mlimuppPr', 'mm', 'mmaddfieldname', 'mmath', 'mmathPict', 'mmathPr', 'mmaxdist', 'mmc', 'mmcJc', 'mmconnectstr',
    'mmconnectstrdata', 'mmcPr', 'mmcs', 'mmdatasource', 'mmheadersource', 'mmmailsubject', 'mmodso', 'mmodsofilter',
    'mmodsofldmpdata', 'mmodsomappedname', 'mmodsoname', 'mmodsorecipdata', 'mmodsosort', 'mmodsosrc', 'mmodsotable',
    'mmodsoudl', 'mmodsoudldata', 'mmodsouniquetag', 'mmPr', 'mmquery', 'mmr', 'mnary', 'mnaryPr', 'mnoBreak', 'mnum',
    'mobjDist', 'moMath', 'moMathPara', 'moMathParaPr', 'mopEmu', 'mphant', 'mphantPr', 'mplcHide', 'mpos', 'mr',
    'mrad',
    'mradPr', 'mrPr', 'msepChr', 'mshow', 'mshp', 'msPre', 'msPrePr', 'msSub', 'msSubPr', 'msSubSup', 'msSubSupPr',
    'msSup',
    'msSupPr', 'mstrikeBLTR', 'mstrikeH', 'mstrikeTLBR', 'mstrikeV', 'msub', 'msubHide', 'msup', 'msupHide', 'mtransp',
    'mtype', 'mvertJc', 'mvfmf', 'mvfml', 'mvtof', 'mvtol', 'mzeroAsc', 'mzeroDesc', 'mzeroWid', 'nesttableprops',
    'nextfile', 'nonesttables', 'objalias', 'objclass', 'objdata', 'object', 'objname', 'objsect', 'objtime',
    'oldcprops',
    'oldpprops', 'oldsprops', 'oldtprops', 'oleclsid', 'operator', 'panose', 'password', 'passwordhash', 'pgp',
    'pgptbl',
    'picprop', 'pict', 'pn', 'pnseclvl', 'pntext', 'pntxta', 'pntxtb', 'printim', 'private', 'propname', 'protend',
    'protstart', 'protusertbl', 'pxe', 'result', 'revtbl', 'revtim', 'rsidtbl', 'rxe', 'shp', 'shpgrp', 'shpinst',
    'shppict', 'shprslt', 'shptxt', 'sn', 'sp', 'staticval', 'stylesheet', 'subject', 'sv', 'svb', 'tc', 'template',
    'themedata', 'title', 'txe', 'ud', 'upr', 'userprops', 'wgrffmtfilter', 'windowcaption', 'writereservation',
    'writereservhash', 'xe', 'xform', 'xmlattrname', 'xmlattrvalue', 'xmlclose', 'xmlname', 'xmlnstbl',
    'xmlopen',     ))

BOLD_STYLE_CONTROL_WORD = frozenset (('b'))
PLAIN_STYLE_CONTROL_WORD = frozenset(('pard', 'plain'))

class RTFParser(object):
    def __init__(self, encoding=RTF_DEFAULT_ENCODING):
        self._encoding = encoding

    def parse(self, text):
        pattern = re.compile(r"\\([a-z]{1,32})(-?\d{1,10})?[ ]?|\\'([0-9a-f]{2})|\\([^a-z])|([{}])|[\r\n]+|(.)", re.I)

        stack = []
        ignorable = False       # Whether this group (and all inside it) are "ignorable".
        is_bold = False
        bold_text = []
        uc_skip = 0             # Number of ASCII characters to skip after a unicode character.
        cur_skip = 0            # Number of ASCII characters left to skip
        out = []                # Output buffer.
        is_plain = False
        for match in pattern.finditer(text):
            control_word, control_word_arg, hex, char, brace, tchar = match.groups()
            if brace:
                cur_skip = 0
                if brace == '{':
                    stack.append((uc_skip, ignorable, is_bold))
                elif brace == '}':
                    uc_skip, ignorable, is_bold = stack.pop()
            elif char:
                cur_skip = 0
                if char == '~':
                    if not ignorable:
                        out.append(u"\xA0")
                elif char in '{}\\':
                    if not ignorable:
                        out.append(char)
                        if is_bold:
                            bold_text.append(char)
                elif char == '*':
                    ignorable = True
            elif control_word:
                #cur_skip = 0
                if control_word in BOLD_STYLE_CONTROL_WORD:
                    is_bold = True
                    is_plain = False
                if control_word in PLAIN_STYLE_CONTROL_WORD:
                    is_plain = True
                if is_plain:
                    is_bold = False
                if control_word in RTF_CONTROL_WORDS:
                    ignorable = True
                elif ignorable:
                    pass
                elif control_word in SPECIAL_CHARS:
                    if bold_text:
                        bold_text.append(SPECIAL_CHARS[control_word])
                    else:
                        out.append(SPECIAL_CHARS[control_word])
                elif control_word == 'uc':
                    uc_skip = int(control_word_arg)
                    cur_skip = uc_skip
                elif control_word == 'u':
                    if cur_skip > 0:
                        cur_skip -= 1
                    else:
                        out.append(self.parse_unicode_char(control_word_arg))
                    cur_skip = uc_skip
            elif hex:
                if cur_skip > 0:
                    cur_skip -= 1
                elif not ignorable:
                    if is_bold:
                        bold_text.append(self.byte_to_unicode_char(hex))
                    else:
                        out.append(self.byte_to_unicode_char(hex))
            elif tchar:
                if cur_skip > 0:
                    cur_skip -= 1
                elif not ignorable:
                    if is_bold:
                        bold_text.append(tchar)
                    else:
                        out.append(tchar)
            if not is_bold:
                if not ignorable:
                    out.extend(bold_text)
                    if bold_text:
                        position = len(out)
                        if ''.join(bold_text).startswith(u"Статья"):
                            out.insert(position, "\n")
                    bold_text = []
        return ''.join(out)

    def byte_to_unicode_char(self, hex):
        c = int(hex, 16)
        if c > 127:
            return (struct.pack('B', c)).decode(self._encoding)
        else:
            return chr(c)

    def parse_unicode_char(self, control_word_arg):
        c = int(control_word_arg)
        if c < 0:
            c += 0x10000
        if c > 127:
            return unichr(c)
        else:
            return chr(c)
