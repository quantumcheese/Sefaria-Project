# -*- coding: utf-8 -*-
import pytest

from .. import texts as t

#todo: simplify this file

def setup_module(module):
    global texts
    global refs
    texts = {}
    refs = {}
    texts['false_pos'] = u"תלמוד לומר (דברים טז, יח) שופטים תתן שוטרים"
    texts['bible_ref'] = u"אם נביא הוא נבואתו מסתלקת ממנו מדבורה דכתיב (שופטים ה, ז) חדלו פרזון בישראל"
    texts['bible_begin'] = u"(שמות כא, ד) אם אדוניו יתן לו אשה"  # These work, even though the presentation of the parens may be confusing.
    texts['bible_mid'] = u"בד (שמות כא, ד) אם אדוניו יתן לו"
    texts['bible_end'] = u"אמר קרא (שמות כא, ד)"
    texts['2ref'] = u"עמי הארץ (דברי הימים ב לב יט), וכתיב (הושע ט ג): לא ישבו בארץ"
    texts['neg327'] = u'שלא לעשות מלאכה ביום הכיפורים, שנאמר בו "כל מלאכה, לא תעשו" (ויקרא טז,כט; ויקרא כג,כח; ויקרא כג,לא; במדבר כט,ז).'
    texts['2talmud'] = u"ודין גזל קורה ובנאה בבירה מה יהא עליה (גיטין נה א). ודין גזל בישוב ורצה להחזיר במדבר (ב''ק קיח א). ודין גזל והקדיש"
    texts['bk-abbrev'] = u"ודין גזל קורה ובנאה בבירה מה יהא עליה (גיטין נה א). ודין גזל בישוב ורצה להחזיר במדבר (ב\"ק קיח א). ודין גזל והקדיש"
    texts['dq_talmud'] = u'(יבמות ס"ה)'
    texts['sq_talmud'] = u""  # Need to find one in the wild
    texts['3dig'] = u'(תהילים קי"ט)'
    texts['2with_lead'] = u'(ראה דברים ד,ז; דברים ד,ח)'
    texts['ignored_middle'] = u'(תהלים לז, א) אל תתחר במרעים ולא עוד אלא שדרכיו מצליחין שנא תהלים י, ה יחילו דרכיו בכל עת ולא עוד אלא שזוכה בדין שנאמר מרום משפטיך מנגדו ולא עוד אלא שרואה בשונאיו שנאמר כל צורריו יפיח בהם איני והאמר ר יוחנן משום רש בן יוחי מותר להתגרות ברשעים בעולם הזה שנא (משלי כח, ד)'


class Test_get_refs_in_text():
    def test_positions(self):
        for a in ['bible_mid', 'bible_begin', 'bible_end']:
            ref = t.get_refs_in_string(texts[a])
            assert 1 == len(ref)
            assert ref[0] == u"שמות כא, ד"

    def test_false_positive(self):
        ref = t.get_refs_in_string(texts['false_pos'])
        assert 1 == len(ref)
        assert ref[0] == u"דברים טז, יח"

    def test_double_ref(self):
        ref = t.get_refs_in_string(texts['2ref'])
        assert 2 == len(ref)
        assert {u'הושע ט ג', u'דברי הימים ב לב יט'} == set(ref)

    ''' includes  ב''ק '''

    def test_double_talmud(self):
        ref = t.get_refs_in_string(texts['2talmud'])
        assert 2 == len(ref)

    ''' includes  ב"ק '''

    def test_double_talmud(self):
        ref = t.get_refs_in_string(texts['bk-abbrev'])
        assert 2 == len(ref)

    def test_out_of_brackets(self):
        ref = t.get_refs_in_string(texts['ignored_middle'])
        assert 2 == len(ref)

    def test_double_quote_talmud(self):
        ref = t.get_refs_in_string(texts['dq_talmud'])
        assert 1 == len(ref)
        assert u'יבמות ס"ה' == ref[0]

    def test_sefer_mitzvot(self):
        ref = t.get_refs_in_string(texts['neg327'])
        assert 4 == len(ref)
        assert {u'ויקרא טז,כט', u'ויקרא כג,כח', u'ויקרא כג,לא', u'במדבר כט,ז'} == set(ref)

    def test_three_digit_chapter(self):
        ref = t.get_refs_in_string(texts['3dig'])
        assert 1 == len(ref)
        assert u'תהילים קי"ט' == ref[0]

    def test_with_lead(self):
        ref = t.get_refs_in_string(texts['2with_lead'])
        assert 2 == len(ref)
        assert {u'דברים ד,ח', u'דברים ד,ז'} == set(ref)

    def test_two_single_quotes(self):
        ref = t.get_refs_in_string(u"עין ממש דכתיב (במדבר ל''ה) ולא תקחו")
        assert 1 == len(ref)
        assert ref[0] == u"במדבר ל''ה"

        ref = t.get_refs_in_string(u"דאמר קרא (שופטים כ י''א) ויאסף כל איש")
        assert 1 == len(ref)
        assert ref[0] == u"שופטים כ י''א"

    def test_spelled_mishnah(self):
        ref = t.get_refs_in_string(u'דתנן (טהרות פ"ג משנה ב) רמ אומר')
        assert 1 == len(ref)
        assert ref[0] == u'טהרות פ"ג משנה ב'