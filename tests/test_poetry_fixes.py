#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test suite for Mishkal tashkeel bug fixes (fix/tashkeel-bugs branch).

Tests each of the 5 fixes:
  1. Word limit increase (1000 -> 20000)
  2. Remove duplicate diacritics + impossible hamza-sukun
  3. Fix missing diacritics in vocalize_foreign for unknown words
  4. Correct spurious shadda on function words
  5. Add sun letter assimilation after definite article
"""

import sys
import os
import re
import json

# Ensure mishkal is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mishkal.tashkeel import TashkeelClass

# Unicode constants for readability
FATHA = '\u064E'
DAMMA = '\u064F'
KASRA = '\u0650'
SHADDA = '\u0651'
SUKUN = '\u0652'
FATHATAN = '\u064B'
DAMMATAN = '\u064C'
KASRATAN = '\u064D'

ALL_HARAKAT = '\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652'
HAMZA_CHARS = '\u0621\u0623\u0625\u0626'  # hamza, hamza-above-alef, hamza-below-alef, hamza-on-ya

# Duplicate diacritic pattern
DUPLICATE_DIACRITIC_RE = re.compile(r'([\u064B-\u0652])\1+')

# Impossible hamza+vowel+sukun pattern
HAMZA_VOWEL_SUKUN_RE = re.compile(r'[\u0621\u0623\u0625\u0626][\u064E-\u0650]\u0652')

# Sun letters
SUN_LETTERS = 'تثدذرزسشصضطظلن'


class TestResults:
    """Collect and report test results."""
    def __init__(self):
        self.results = []
        self.pass_count = 0
        self.fail_count = 0

    def record(self, fix_num, test_name, passed, detail=""):
        status = "PASS" if passed else "FAIL"
        self.results.append({
            'fix': fix_num,
            'test': test_name,
            'status': status,
            'detail': detail
        })
        if passed:
            self.pass_count += 1
        else:
            self.fail_count += 1
        symbol = "+" if passed else "X"
        print(f"  [{symbol}] {test_name}")
        if detail:
            for line in detail.split('\n'):
                print(f"      {line}")

    def summary(self):
        total = self.pass_count + self.fail_count
        print(f"\n{'='*60}")
        print(f"RESULTS: {self.pass_count}/{total} passed, {self.fail_count} failed")
        print(f"{'='*60}")
        return self.fail_count == 0


def create_vocalizer():
    """Create and configure a TashkeelClass instance."""
    v = TashkeelClass()
    # On master the default limit is 1000; we keep it to test Fix 1 honestly
    # But for other tests we need it to work, so set it to 20000
    # Actually, for Fix 1 we test separately with default limit
    v.set_limit(20000)
    return v


def strip_harakat(text):
    """Remove all diacritical marks from Arabic text."""
    return re.sub(f'[{ALL_HARAKAT}]', '', text)


# =============================================================
# Fix 1: Word limit increase (1000 -> 20000)
# =============================================================
def test_fix1_word_limit(vocalizer, results):
    print("\n--- Fix 1: Word limit (>1000 words) ---")

    # For this test, we create a NEW vocalizer with the DEFAULT limit
    # to test whether the default is sufficient
    default_v = TashkeelClass()
    # Don't call set_limit - use the default

    lines = [
        "على قدر أهل العزم تأتي العزائم",
        "وتأتي على قدر الكرام المكارم",
        "وتعظم في عين الصغير صغارها",
        "وتصغر في عين العظيم العظائم",
        "يكلف سيف الدولة الجيش همه",
        "وقد عجزت عنه الجيوش الخضارم",
        "إذا لم يكن من الموت بد فمن العجز أن تموت جبانا",
        "قف على ناصية الأمل وناد على القمة",
        "فإن العلم نور والجهل ظلام",
        "ومن يتهيب صعود الجبال يعش أبد الدهر بين الحفر",
    ]

    # Repeat enough to exceed 1500 characters
    long_text = "\n".join(lines * 20)
    char_count = len(long_text)
    word_count = len(long_text.split())

    result = default_v.tashkeel(long_text)

    result_stripped = strip_harakat(result).strip()
    input_stripped = strip_harakat(long_text).replace('\n', ' ').strip()

    result_words = result_stripped.split()
    input_words = input_stripped.split()

    ratio = len(result_words) / len(input_words) if input_words else 0

    passed = ratio >= 0.90
    detail = (f"Input: {char_count} chars, {len(input_words)} words\n"
              f"Output: {len(result_words)} words (ratio: {ratio:.2f})")
    results.record(1, "Long text (>1500 chars) fully diacritized", passed, detail)


# =============================================================
# Fix 2: Remove duplicate diacritics
# =============================================================
def test_fix2_duplicate_diacritics(vocalizer, results):
    print("\n--- Fix 2: Duplicate diacritics removal ---")

    test_texts = [
        "كالرجل المجتهد في عمله",
        "والفتاتان المجتهدتان في دراستهما",
        "للعالمين رحمة وبركة",
        "بالعلم والإيمان ترتقي الأمم",
        "فالكتابان مفيدان للقارئ",
    ]

    for text in test_texts:
        result = vocalizer.tashkeel(text)
        matches = DUPLICATE_DIACRITIC_RE.findall(result)
        passed = len(matches) == 0
        detail = f"Input:  {text}\nOutput: {result}"
        if not passed:
            detail += f"\nDuplicate marks found: {matches}"
        results.record(2, f"No duplicate diacritics: '{text[:30]}...'", passed, detail)


# =============================================================
# Fix 3: Impossible hamza+sukun combination
# =============================================================
def test_fix3_hamza_sukun(vocalizer, results):
    print("\n--- Fix 3: Impossible hamza+vowel+sukun ---")

    test_texts = [
        "إن العلم نور",
        "أنت الأول",
        "إلى الله المصير",
        "أبو بكر الصديق",
        "رئيس الوزراء",
    ]

    for text in test_texts:
        result = vocalizer.tashkeel(text)
        matches = HAMZA_VOWEL_SUKUN_RE.findall(result)
        passed = len(matches) == 0
        detail = f"Input:  {text}\nOutput: {result}"
        if not passed:
            for m in HAMZA_VOWEL_SUKUN_RE.finditer(result):
                span = result[max(0, m.start()-2):m.end()+2]
                detail += f"\nImpossible combo at pos {m.start()}: '{span}' => {[hex(ord(c)) for c in m.group()]}"
        results.record(3, f"No hamza+vowel+sukun: '{text[:30]}'", passed, detail)


# =============================================================
# Fix 4: Spurious shadda on function words
# =============================================================
def test_fix4_spurious_shadda(vocalizer, results):
    print("\n--- Fix 4: Spurious shadda on function words ---")

    function_word_tests = [
        {
            'text': "ذهب على الطريق",
            'bad_pattern': 'عَلَّى',
            'good_pattern': 'عَلَى',
            'label': 'على (ala)'
        },
        {
            'text': "ذهب إلى البيت",
            'bad_pattern': 'إِلَّى',
            'good_pattern': 'إِلَى',
            'label': 'إلى (ila)'
        },
        {
            'text': "على قدر أهل العزم",
            'bad_pattern': 'عَلَّى',
            'good_pattern': 'عَلَى',
            'label': 'على in poetry'
        },
        {
            'text': "مشى إلى المسجد",
            'bad_pattern': 'إِلَّى',
            'good_pattern': 'إِلَى',
            'label': 'إلى in sentence'
        },
    ]

    for test in function_word_tests:
        result = vocalizer.tashkeel(test['text'])
        has_bad = test['bad_pattern'] in result
        passed = not has_bad
        detail = f"Input:  {test['text']}\nOutput: {result}\nChecking no '{test['bad_pattern']}' present"
        if has_bad:
            detail += f"\nFOUND spurious shadda: '{test['bad_pattern']}'"
        results.record(4, f"No spurious shadda: {test['label']}", passed, detail)


# =============================================================
# Fix 5: Sun letter assimilation after definite article
# =============================================================
def test_fix5_sun_letter_assimilation(vocalizer, results):
    print("\n--- Fix 5: Sun letter assimilation ---")

    sun_letter_tests = [
        {
            'text': "الشمس ساطعة",
            'sun_word_stripped': 'الشمس',
            'sun_letter': 'ش',
            'label': 'الشمس (ash-shams)'
        },
        {
            'text': "جاء الناس إلى المسجد",
            'sun_word_stripped': 'الناس',
            'sun_letter': 'ن',
            'label': 'الناس (an-nas)'
        },
        {
            'text': "في الدنيا والآخرة",
            'sun_word_stripped': 'الدنيا',
            'sun_letter': 'د',
            'label': 'الدنيا (ad-dunya)'
        },
        {
            'text': "بسم الله الرحمن الرحيم",
            'sun_word_stripped': 'الرحمن',
            'sun_letter': 'ر',
            'label': 'الرحمن (ar-rahman)'
        },
        {
            'text': "السلام عليكم",
            'sun_word_stripped': 'السلام',
            'sun_letter': 'س',
            'label': 'السلام (as-salam)'
        },
        {
            'text': "الطريق طويل",
            'sun_word_stripped': 'الطريق',
            'sun_letter': 'ط',
            'label': 'الطريق (at-tariq)'
        },
        {
            'text': "اللغة العربية جميلة",
            'sun_word_stripped': 'اللغة',
            'sun_letter': 'ل',
            'label': 'اللغة (al-lugha)'
        },
    ]

    for test in sun_letter_tests:
        result = vocalizer.tashkeel(test['text'])
        sun = test['sun_letter']
        pattern = re.compile(f'ال[{ALL_HARAKAT}]?{re.escape(sun)}[{ALL_HARAKAT}]*')
        match = pattern.search(result)
        if match:
            matched_text = match.group()
            has_shadda = SHADDA in matched_text[matched_text.index(sun):]
            passed = has_shadda
        else:
            passed = False
            matched_text = "NOT FOUND"

        detail = f"Input:  {test['text']}\nOutput: {result}\nMatched: {matched_text}\nSun letter '{sun}' has shadda: {passed}"
        results.record(5, f"Sun letter shadda: {test['label']}", passed, detail)


# =============================================================
# End-to-end real poem test
# =============================================================
def test_real_poem(vocalizer, results):
    print("\n--- End-to-end: Al-Mutanabbi poem ---")

    poem = """على قدر أهل العزم تأتي العزائم
وتأتي على قدر الكرام المكارم
وتعظم في عين الصغير صغارها
وتصغر في عين العظيم العظائم"""

    result = vocalizer.tashkeel(poem)
    print(f"  Input:\n{poem}")
    print(f"  Output:\n{result}")

    harakat_count = sum(1 for c in result if c in ALL_HARAKAT)
    passed_has_harakat = harakat_count > 20
    results.record(0, f"Poem has diacritics ({harakat_count} marks)", passed_has_harakat,
                   f"Found {harakat_count} diacritical marks in output")

    dup_matches = DUPLICATE_DIACRITIC_RE.findall(result)
    passed_no_dups = len(dup_matches) == 0
    results.record(0, "Poem has no duplicate diacritics", passed_no_dups,
                   f"Duplicate marks: {dup_matches}" if dup_matches else "Clean")

    hamza_matches = HAMZA_VOWEL_SUKUN_RE.findall(result)
    passed_no_hamza = len(hamza_matches) == 0
    results.record(0, "Poem has no impossible hamza+sukun", passed_no_hamza,
                   f"Bad combos: {hamza_matches}" if hamza_matches else "Clean")

    return result


def main():
    print("=" * 60)
    print("Mishkal Tashkeel Bug Fixes - Test Suite")
    print("=" * 60)

    branch = "unknown"
    try:
        import subprocess
        branch = subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            cwd=os.path.join(os.path.dirname(__file__), '..'),
            text=True
        ).strip()
    except Exception:
        pass
    print(f"Branch: {branch}")

    results = TestResults()
    vocalizer = create_vocalizer()

    test_fix1_word_limit(vocalizer, results)
    test_fix2_duplicate_diacritics(vocalizer, results)
    test_fix3_hamza_sukun(vocalizer, results)
    test_fix4_spurious_shadda(vocalizer, results)
    test_fix5_sun_letter_assimilation(vocalizer, results)
    poem_result = test_real_poem(vocalizer, results)

    all_passed = results.summary()

    output = {
        'branch': branch,
        'pass_count': results.pass_count,
        'fail_count': results.fail_count,
        'results': results.results,
        'poem_output': poem_result,
    }
    json_path = os.path.join(os.path.dirname(__file__), f'test_results_{branch.replace("/", "_")}.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nResults saved to: {json_path}")

    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
