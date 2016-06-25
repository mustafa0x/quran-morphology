# Quran Morphology

This is a fork of [Quranic Arabic Corpus Morphology v0.4](http://corpus.quran.com),
"an annotated linguistic resource which shows the Arabic grammar,
syntax and morphology for each word in the Holy Quran".

The data here can be seen (in Arabic) at [furqan.co](furqan.co)
([example root](http://furqan.co/#w=أتي&src=quran-roots),
[example ayah morphology](http://furqan.co/#s=1&a=1&src=ayah-morph))
while v0.4 can be seen at [corpus.quran.com](corpus.quran.com)
([example root](http://corpus.quran.com/qurandictionary.jsp?q=Aty),
[example ayah morphology](http://corpus.quran.com/wordbyword.jsp?chapter=1&verse=1#(1:1:1))).

- [quran-morphology.txt](quran-morphology.txt) can be reproduced by running [bw-to-ar.py](scripts/bw-to-ar.py)
  against [`quranic-corpus-morphology-0.4.txt`](http://corpus.quran.com/download/)
  then [apply-changes.py](scripts/apply-changes.py) against the outputted file.
- [morphology-terms.json](morphology-terms.json) contains the terms used in
  [quran-morphology.txt](quran-morphology.txt) with their respective meanings in Arabic.

## Changes
- Added roots to several words, especially four-letter words and PNs.
- Many root and lemma fixes, especially spelling issues.
- Split ئذ from يومئذ, and set the root of يوم.
- Fixed many incorrectly-tagged occurrences of كَم and أي.
- Removed gender from all dual pronouns - except PERF's
  subject pronoun - as they're gender indifferent.
- Tag هَ prefix as ATT, instead of VOC.
- Mark هَا of أيّها as ATT.
- إذا: mark as ANS if tanween exists; retagged many occurrences
  from T to SUR.
- DEMs: separate and mark ATT prefix, and DIST and ADDR suffix.
- Mark the 13 أسماء الأفعال as NV (VN would possibly be more accurate
  but that's taken for مصدر). NV supersedes IMPN, as IMPN is only a single tense.
- Change INTG and EQ ا to أ.
- Fixed lemma of لما (was لم in some occurrences).
- Removed parentheses around ayah numbers.
- Replaced all Buckwalter with the respective Arabic.
- Made form I and IND explicit. This is especially important
  as some verbs don't fit under any of the normal verb forms,
  like نِعم and بِئس.

Among many other changes; see [apply-changes.py](scripts/apply-changes.py)
for what exactly was changed and how.

### Tag Changes
- Added NV (اسم فعل), as mentioned above.
- Retag ADJ as N, and mark as ADJ in attributes.
- Added ATT (e.g. ه in هذا).
- Added DIST (e.g. ل in ذلك).
- Added ADDR (e.g. ك in ذلك).
- Replace ACT|PCPL and PASS|PCPL with ACT_PCPL and PASS_PCPL.

## To Do
- **Mark the form of all nouns.**
  Currently, only verbs have their form set, as well as most
  nouns derived from one of the 10 verbal forms.
  On top of this, all other nounal forms should be marked.
  For example: الرحمن should be marked as فعلان, while
  الرحيم should be marked as فعيل, and أرحم should be marked as أفعل.
  Also, most verbal nouns are not marked as so, e.g. the second ayah
  of Surat al-Baqarah has two unmarked verbal nouns (الكتاب، هدى) which
  should be properly tagged.
- The lemmas need a fair amount of reviewing. Some of the issues:
  - Lemmas should be spelled in Imlaaiee, not Uthamni.
  - Lemmas should be returned to singular, male.
  - Some lemmas incorrectly end with 'ت' which it is to mark feminine.
    E.g. the lemma of 2:16:7:1 is رَبِحَت, while it should be رَبِحَ.
- The second predicate (خبر ثان) is often marked as ADJ. E.g. the 12th word of 2:115
  shouldn't be ADJ as grammatically it is the same as the preceding noun.
- Remove most person, gender, and number tagging from verbs, as
  verbs in Arabic rarely carry this information, if ever. What
  does carry such information is the pronoun attached to the verb.
  The main exception to this is the imperfect verb that starts with:
  - أ, as it (only) necessitates 1st person and singular,
  - ن, as it (only) necessitates 1st person (yet can be dual or plural),
  - or ي, as it (only) necessitates 3rd person.
- General review; many other issues exist.

### Multiple Tags
Mark particles or words which have shared traits. For example:
- The following are LOC-DEM هُنَا، هُنَالِك، ثم.
- أين is either LOC-INTG or LOC-COND.
- متى is T-INTG.
- COND and INTG are usually nouns, and sometimes particles.
  Mark each occurrence accordingly.
