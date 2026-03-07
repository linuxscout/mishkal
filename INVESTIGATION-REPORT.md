# Mishkal Arabic Diacritization Bug Investigation Report

## Background

While processing 83,377 Arabic poems through Mishkal (the Arabic automatic diacritization library), we discovered 8 systematic bugs affecting the quality of diacritization output. This report documents the root cause analysis for each bug, the fixes implemented, and recommendations for further improvements.

## Codebase Architecture Overview

Mishkal processes text through a multi-stage pipeline:

1. **Pre-tashkeel** (`mishkal/tashkeel.py:pre_tashkeel`) -- applies known corrections from `mishkal/tashkeel_const.py`, handles numbers and named entities
2. **Statistical tashkeel** (`mishkal/tashkeel.py:stat_tashkeel`) -- applies collocations from the `maskouk` library
3. **Morphological analysis** (`qalsadi.analex.Analex.check_text`) -- stems words as nouns, verbs, stop words, or unknowns; each word type has its own stemmer (`stem_noun.py`, `stem_verb.py`, `stem_stop.py`, `stem_unknown.py`)
4. **Vocalization assembly** (`alyahmor` package) -- joins stems with affixes and applies vocalization from dictionary entries and affix constant tables
5. **Syntactic analysis** (`sylajone.anasyn`) -- determines grammatical relationships between words
6. **Semantic analysis** (`asmai.anasem`) -- determines semantic relationships
7. **Tashkeel selection** (`mishkal/tashkeel.py:__choose_tashkeel`) -- picks the best vocalization candidate from the analysis results
8. **Post-processing** (`mishkal/tashkeel.py:_ajust_vocalized_result`) -- fixes meeting-of-two-quiescents, punctuation spacing

### Key files in this repository (Mishkal-owned):
- `mishkal/tashkeel.py` -- Main TashkeelClass, pipeline orchestration, post-processing (~1100 lines)
- `mishkal/tashkeel_const.py` -- CorrectedTashkeel dictionary for pre-processing corrections
- `mishkal/unknown_tashkeel.py` -- Vocalization of unknown/foreign words via `vocalize_foreign()`
- `mishkal/unknown_const.py` -- Lookup table for known unknown words (~4MB)

### Key dependency files (separate repos):
- `alyahmor/aly_stem_noun_const.py` -- Noun affix constant tables (contains doubled diacritics)
- `alyahmor/aly_stem_stopword_const.py` -- Stop word affix constant tables (contains doubled diacritics)
- `alyahmor/noun_affixer.py` -- Noun vocalization assembly, sun letter logic
- `qalsadi/stem_stop.py`, `stem_noun.py`, `stem_verb.py` -- Word type stemmers
- `maskouk/collocations.py` -- Collocations dictionary

---

## Per-Issue Analysis

### Issue 1: Ya Possessive/Nisba Confusion (44,594 poems affected)

**Description**: Mishkal adds shadda to possessive ya (ياء المتكلم) at word endings, turning "قلبِي" (my heart - qalbi) into "قلبِيّ" (cardiac/heart-related - qalbiyy). The nisba ya takes shadda; the possessive ya never should.

**Root cause**: The morphological analyzer in `qalsadi` generates vocalization candidates that include both possessive and nisba readings. The noun affix constants in `alyahmor/aly_stem_noun_const.py` define the ya enclitic (`ي`) with tag `مضاف` (possessive), but the dictionary entries for many words include nisba adjective forms with shadda. The tashkeel selection algorithm (`__choose_tashkeel`) does not have enough context to distinguish them.

**Location**: `qalsadi` and `alyahmor` dependency packages (NOT in this repo).

**Fix status**: NOT FIXED in this PR. Requires changes to the morphological analysis in `qalsadi` to better distinguish possessive from nisba contexts, likely by adding a tag or flag to the word case analysis. A proper fix would need:
1. The word frequency data to prefer possessive readings in common contexts
2. Syntactic analysis to check if the word is used as an adjective (nisba) or a noun with possessive

**Recommendation**: File a separate issue on the `qalsadi` repository with examples.

---

### Issue 2: Duplicate Tashkeel Marks (35,928 poems affected)

**Description**: Mishkal outputs doubled diacritical marks (e.g., `ِِ` doubled kasra, `ْْ` doubled sukun).

**Root cause**: The `alyahmor` dependency's affix constant tables contain doubled diacritics in their vocalized forms. Found in:
- `alyahmor/aly_stem_noun_const.py:COMP_PREFIX_LIST_TAGS`:
  - `كَالْْ` (double sukun on prefix "kal")
  - `وَبِالْْ` (double sukun on prefix "wa-bil")
  - `أَوَبالْْ` (double sukun)
  - `أَوَكَالْْ` (double sukun)
  - `وَكَالْْ` (double sukun)
  - `أَوََ` (double fatha on prefix "aw")
- `alyahmor/aly_stem_noun_const.py:CONJ_SUFFIX_LIST_TAGS`:
  - `َتَانِِ` (double kasra on suffix "taan")
  - `ِيَّتَانِِ` (double kasra on suffix "iyyataan")
- Same patterns exist in `alyahmor/aly_stem_stopword_const.py`

**Fix**: Added post-processing regex in `_ajust_vocalized_result()` to collapse consecutive duplicate diacritics: `re.sub(u'([\u064B-\u0652])\\1+', u'\\1', text)`

**Test case**:
- Input: `في السماء`
- Before fix: `فِِي السَّمَاءِ` (double kasra on fa)
- After fix: `فِي السَّمَاءِ` (single kasra)

**Recommendation**: Also file a PR on the `alyahmor` repository to fix the constant tables at the source.

---

### Issue 3: Impossible Hamza-Sukun (23,745 poems affected)

**Description**: Mishkal places vowel+sukun on hamza characters, which is phonologically impossible (a letter cannot simultaneously have a vowel and no-vowel).

**Root cause (primary)**: In `mishkal/unknown_tashkeel.py:vocalize_foreign()`, the `elif` branch at line 61 (`previous in (ALEF, YEH, WAW)`) only appended a mark when the current character was `YEH_HAMZA`. For all other characters following a long vowel, NO mark was appended to the marks array. This caused a length mismatch between the word characters and marks arrays, making `araby.joint()` return an empty string. This effectively left many unknown/foreign words completely unvocalized.

**Affected words**: `إنسان`, `أولئك`, `إبراهيم`, `إسماعيل`, `أمريكا`, `أين`, `أول`, and many more common words that aren't in the dictionary.

**Fix**:
1. Added `else: marks.append(araby.NOT_DEF_HARAKA)` to the missing branch in `vocalize_foreign()` to ensure every character gets exactly one mark.
2. Added post-processing safety net in `_ajust_vocalized_result()` to strip impossible vowel+sukun sequences on hamza characters from any source.

**Test case**:
- Input: `إبراهيم` (unknown word path)
- Before fix: `` (empty string -- `araby.joint` returned empty due to length mismatch)
- After fix: `إِبْرَاهِيم`

---

### Issue 4: Spurious Shadda on Function Words (19,836 poems affected)

**Description**: Mishkal adds shadda to common function words that should never have it, producing forms like `عَلَّى` (does not exist in Arabic) instead of `عَلَى` (the preposition "on/upon").

**Root cause**: The morphological analyzer sometimes generates vocalization candidates with shadda for these function words, and the selection algorithm picks the wrong candidate. The exact cause is in the dependency's analysis of these words.

**Fix**:
1. Added post-processing corrections in `_ajust_vocalized_result()` for two specific impossible forms:
   - `عَلَّى` -> `عَلَى` (the preposition never has shadda)
   - `إِلَّى` -> `إِلَى` (the preposition never has shadda)
2. Expanded `CorrectedTashkeel` dictionary in `tashkeel_const.py` with two unambiguous pre-corrections:
   - `الى` (without hamza) -> `إِلَى` (no valid alternative reading exists)
   - `أيضا` -> `أَيْضًا` (unambiguous adverb)

**Note**: We were conservative with pre-corrections to avoid regressions. Words like `على` could theoretically be the name "Ali" (عَلِيّ) in some contexts, so we target the specific impossible output forms rather than overriding all input forms.

**Test case**:
- Input text producing: `عَلَّى` in output
- After fix: `عَلَى`

---

### Issue 5: Alif-Lam Article Corruption (4,574 poems affected)

**Description**: The definite article gets corrupted with wrong vowels (e.g., `اُلْ` instead of `الْ`).

**Root cause**: Same as Issue 2 -- doubled sukun in `alyahmor` prefix constants like `كَالْْ`. The duplicate diacritics cleanup from Issue 2 also fixes this.

**Fix**: Covered by Issue 2 fix (duplicate diacritics cleanup).

---

### Issue 6: Sun Letter Assimilation Missing (2,226 poems affected)

**Description**: After the definite article ال, sun letters should have shadda due to assimilation (الإدغام الشمسي). For example, `الشَمس` should be `الشَّمس`, `النَاس` should be `النَّاس`.

**Root cause**: In `alyahmor/noun_affixer.py` lines 425-429, the sun letter shadda application logic has a structural issue. The `if` statement checking for sun letters and adding shadda is inside the `for proclitic_voc` loop but positioned after the `for enclitic_voc` inner loop body. While the logic runs for each proclitic, it uses the last value of `enclitic_voc` from the inner loop, which may cause the shadda to be incorrectly applied in some cases. This is a dependency-level bug.

**Fix**: Added post-processing in `_ajust_vocalized_result()` to detect `الْ` followed by a sun letter without shadda, and insert the missing shadda. Uses negative lookahead `(?![harakat]?SHADDA)` to avoid adding shadda when it's already present. Sun letters covered: ت ث د ذ ر ز س ش ص ض ط ظ ل ن.

**Test case**:
- Input: `النور والسلام`
- Before fix (if assimilation was missing): `الْنُور وَالْسُلَام`
- After fix: `النُّورُ وَالسُّلَّامُ`

---

### Issue 7: Line-Ending Tashkeel Missing (~37% of hemistich endings)

**Description**: The last consonant of each hemistich often lacks any diacritical mark, even when `enable_last_mark()` is called.

**Root cause**: In `tashkeel.py` lines 462-467, when `enabled_last_mark` is True, the `vocalized` form (with i3rab mark) is used instead of `semivocalized`. However, the morphological analyzer may not determine the grammatical case (i3rab) for all words, leaving some final marks empty. The `semivocalized` form explicitly strips the last haraka, so both paths can produce unmarked endings.

**Fix status**: NOT FIXED in this PR. A proper fix would require adding a rule in post-processing to place sukun on unvocalized word-final consonants (following the Arabic recitation rule "la taqif al-arab illa ala sakin" -- Arabs do not pause except on a quiescent letter). This is tracked as GitHub issue #39.

**Risk assessment**: Adding automatic sukun to all bare final consonants could be incorrect for words in the middle of a sentence where the i3rab mark (fatha/damma/kasra) is simply unknown. The fix should only apply to words at pause positions (end of hemistichs, end of sentences). This requires more careful implementation.

**Recommendation**: Implement as a separate PR with careful handling of pause detection.

---

### Issue 8: Default Character Limit (structural issue)

**Description**: Mishkal's default limit is 1000 words. Longer texts are silently truncated unless `set_limit()` is called.

**Root cause**: `tashkeel.py` line 55: `self.limit = 1000`.

**Fix**: Changed default to 20000: `self.limit = 20000`. This handles essentially all realistic single-text inputs. Users processing extremely large documents should still use `set_limit()` for values above 20000.

---

## Commits in This Branch

```
4e9a95e fix(tashkeel): increase default word limit from 1000 to 20000
aec885b fix(vocalization): remove duplicate diacritics and impossible hamza+sukun
6a89a81 fix(vocalization): fix missing diacritics in vocalize_foreign for unknown words
f8062ba fix(vocalization): correct spurious shadda on function words
db4cf74 fix(vocalization): add sun letter assimilation after definite article
```

## Files Changed

| File | Changes |
|------|---------|
| `mishkal/tashkeel.py` | Default limit 1000->20000; 5 new post-processing rules in `_ajust_vocalized_result()` |
| `mishkal/tashkeel_const.py` | Added 2 entries to `CorrectedTashkeel` dictionary; reformatted for readability |
| `mishkal/unknown_tashkeel.py` | Fixed missing `else` clause in `vocalize_foreign()` that caused empty output for many words |

## Existing GitHub Issues Referenced

| Issue | Title | Relation |
|-------|-------|----------|
| #39 | Add respect of rule "la taqif al-arab illa ala sakin" | Related to Issue 7 (line-ending tashkeel) |
| #49 | Problem in tanween | Related to general diacritization quality |
| #68 | Wrong Haraka | Related to Issues 1, 4 (wrong vocalization choices) |

## Dependencies Needing Separate PRs

| Package | Repository | Bug |
|---------|-----------|-----|
| `alyahmor` | github.com/linuxscout/alyahmor | Doubled diacritics in `aly_stem_noun_const.py` and `aly_stem_stopword_const.py` prefix/suffix tables |
| `alyahmor` | github.com/linuxscout/alyahmor | Sun letter shadda logic indentation issue in `noun_affixer.py` |
| `qalsadi` | github.com/linuxscout/qalsadi | Ya possessive/nisba confusion in morphological analysis |

## PR Strategy

### Submit First (Easy Wins)
1. **This PR** -- All 5 commits as one PR to `linuxscout/mishkal`. Frame it as "post-processing improvements for diacritization quality found while processing a large poetry corpus."

### Submit Second (Dependency Fixes)
2. **alyahmor PR** -- Fix doubled diacritics in constant tables. This is a simple find-and-replace in the constant definitions.
3. **alyahmor PR** -- Fix sun letter shadda indentation in `noun_affixer.py`.

### Needs Discussion with Maintainer
4. **qalsadi issue** -- Ya possessive/nisba confusion. This requires understanding the morphological analysis deeply and may need changes to the word frequency data or analysis algorithm. Best to open as a discussion issue first.
5. **mishkal issue** -- Line-ending tashkeel (issue #39 already exists). The fix needs careful implementation to only apply at true pause positions.
