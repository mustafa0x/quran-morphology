# -*- coding: utf-8
from __future__ import unicode_literals
import io
import re
"""
Applies changes to quranic-corpus-morphology-0.4-ar.txt.

See: https://github.com/mustafa0x/quran-morphology
"""

def split_dem(m):
    addr_forms = {'كَ': 'M', 'كِ': 'F', 'كُمَا': 'D', 'كُم': 'MP', 'كُنَّ': 'FP'}
    tpl = '\n%s%s\t%s\t%s\tSUFFIX|+%s'
    out = m.expand(r'\1\2\3\6')
    i = int(m.group(2)) + 1
    if m.group(4):
        out += tpl % (m.group(1), i, m.group(4), 'DIST', 'ل:DIST')
        i += 1
    addr = m.group(5)
    # كُم has different ending harakaat
    form = addr_forms[addr[:3]] if addr[:3] == 'كُم' and len(addr) < 5 else addr_forms[addr]
    return out + tpl % (m.group(1), i, addr, 'ADDR', 'ADDR:') + form

verb_forms = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI']

fixes = [
    # ADJ is not a specific form of noun,
    # rather it is dependent on where it is in the sentence.
    (0, '\tADJ\tSTEM|POS:ADJ', '\tN\tSTEM|POS:N|ADJ'),

    # ACT|PCPL, PASS|PCPL -> ACT_PCPL, PASS_PCPL
    (1, '(ACT|PASS)\|(PCPL)', r'\1_\2'),

    # Change INTG and EQ alif to hamza
    (0, 'ا:', 'أ:'),

    # Root fixes
    (0, 'ROOT:لالا', 'ROOT:لؤلؤ'),
    (0, 'ROOT:نوس', 'ROOT:أنس'),
    (0, 'ROOT:ندو', 'ROOT:ندي'),  # Fix root of نداء, etc.
    (0, 'PN|LEM:عَاد|ROOT:عود', 'PN|LEM:عَاد|ROOT:عدو'),  # The root of عاد is عدو
    (0, 'ROOT:معن', 'ROOT:عون'),

    # Make implicit attributes explicit
    # IMPF: mark as IND if MOOD not set
    (1, r'(IMPF.*\|[1-3]?[MF]?[SDP]?(?!MOOD:.*))\n', r'\1|MOOD:IND\n'),
    # Verbs: mark as form I if form not set
    (1, r'((PERF|IMPF|IMPV)\|((?!(PASS\|)?\()|PASS\|(?!\()))', r'\1(I)|'),
    # VN/ACT_PCPL/PASS_PCPL: mark as form I if form not set
    (1, r'((VN|ACT_PCPL|PASS_PCPL)\|(?!\())', r'\1(I)|'),

    # Root & Lemma spelling fixes:
    # Replace ا with أ in roots
    (0, 'ROOT:ا', 'ROOT:أ'),
    (1, r'(ROOT:.)ا(.\|)', r'\1أ\2'),
    (1, r'(ROOT:..)ا\|', r'\1أ|'),
    (0, 'ROOT:هأت', 'ROOT:هات'),  # An exception to the above
    # Remove Uthmani spelling for lemmas
    (0, 'LEM:ٱ', 'LEM:ا'),
    (0, 'LEM:آ', 'LEM:آ'),
    (0, 'LEM:ءَا', 'LEM:آ'),
    (0, 'LEM:كَى', 'LEM:كَي'),
    (0, 'LEM:رَءَا', 'LEM:رَأَى'),
    (1, r'(LEM:لَدَ)ي', r'\1ى'),
    (0, 'LEM:إِين', 'LEM:إِن'),
    # Remove '2' from lemmas; the root distinguishes
    (1, r'(LEM:[^|\n]+)2', r'\1'),
    # Remove ّ from first letter of lemma (caused by idghaam or اللام الشمسية)
    (1, r'(?<=LEM:.)ّ', ''),
    # عظام LEM from عظيم to عظام
    (1, r'(عِظَ[اٰ]م.*)عَظِيم(.*)', r'\1عِظَام\2'),

    # Set the root for several words
    (0, 'LEM:أَبَارِيق', 'LEM:أَبَارِيق|ROOT:برق'),
    (0, 'LEM:نَمَارِق', 'LEM:نَمَارِق|ROOT:نمرق'),
    (0, 'LEM:بَرْزَخ', 'LEM:بَرْزَخ|ROOT:برزخ'),
    (0, 'LEM:زَرَابِىّ', 'LEM:زَرَابِىّ|ROOT:زرب'),
    (0, 'LEM:عَرَفَٰت', 'LEM:عَرَفَٰت|ROOT:عرف'),
    (0, 'LEM:الْعُزَّىٰ', 'LEM:الْعُزَّىٰ|ROOT:عزز'),
    (0, 'LEM:آدَم', 'LEM:آدَم|ROOT:أدم'),
    (0, 'LEM:رَمَضَان', 'LEM:رَمَضَان|ROOT:رمض'),
    (0, 'LEM:سَبَإ', 'LEM:سَبَإ|ROOT:سبأ'),
    (0, 'LEM:يَحْيَىٰ', 'LEM:يَحْيَىٰ|ROOT:حيي'),
    (0, 'LEM:قُرَيْش', 'LEM:قُرَيْش|ROOT:قرش'),
    (0, 'LEM:مَدْيَن', 'LEM:مَدْيَن|ROOT:مدن'),
    (0, 'LEM:مَرْوَة', 'LEM:مَرْوَة|ROOT:مرو'),
    (0, 'LEM:مَسِيح', 'LEM:مَسِيح|ROOT:مسح'),
    (0, 'LEM:مَنَوٰة', 'LEM:مَنَوٰة|ROOT:مني'),
    (0, 'LEM:جُودِىّ', 'LEM:جُودِىّ|ROOT:جود'),
    (1, r'(LEM:مُحَمَّد|LEM:أَحْمَد)', r'\1|ROOT:حمد'),
    (1, r'(LEM:ـَٰٔن)', r'\1|ROOT:أون'),  # الآن
    (0, 'LEM:يَهُودِيّ', 'LEM:يَهُود|ROOT:هود'), # Fix LEM, add root

    # Remove gender from all dual pronouns - except PERF's subject
    # pronoun - as they're gender indifferent.
    (1, r'((IMPF|IMPV|POS:[^V]).*\n.*PRON:\d?)[MF]D', r'\1D'),

    # اطمأنّ is quad, IV
    (0, 'ROOT:طمن', 'ROOT:طمأن'),
    (0, 'XII', 'IV'),

    # REL fixes
    # الذي is never COND
    (0, 'COND\tSTEM|POS:COND|LEM:الَّذِى', 'REL\tSTEM|POS:REL|LEM:الَّذِى'),
    # اللائي LEM: الذي
    (0, 'LEM:الَّٰٓـِٔى', 'LEM:الَّذِى'),

    # إلا is never CERT, the 4 matching occurrences are RES
    (1, r'CERT(\tSTEM\|POS:)CERT(\|LEM:إِلَّا)', r'RES\1RES\2'),

    # هَ is ATT, not VOC
    (0, 'VOC\tPREFIX|هَ', 'ATT\tPREFIX|هَ'),
    # ألا is primarily ATT
    (0, 'INC\tSTEM|POS:INC|LEM:أَلَآ', 'ATT\tSTEM|POS:ATT|LEM:أَلَآ'),

    # ذو (possessive, one of the "five" names): fix LEM
    (0, 'POS:N|LEM:ذَا|', 'POS:N|LEM:ذُو|'),
    (1, r'(2:177:23:1.*\|M)D(.*)', r'\1P\2'),
    (0, 'LEM:أُولِى|ROOT:أول', 'LEM:ذُو'),

    # Split ئذ from يومئذ, set root of يوم
    (1, r'([\d:]+):1(\tيَوْم[َِ])(ئِذٍ)(.*)يَوْمَئِذ(.*)', r'\1:1\2\4يَوْم|ROOT:يوم\5\n\1:2\t\3\4إِذ'),
    (1, r'([\d:]+):2(\tيَوْم[َِ])(ئِذٍ)(.*)يَوْمَئِذ(.*)', r'\1:2\2\4يَوْم|ROOT:يوم\5\n\1:3\t\3\4إِذ'),

    (0, 'ROOT:مرر|MD', 'ROOT:مرر|FD'), # مرتان is F

    # كَم fixes
    (0, r'LEM:كَم|NOM', 'LEM:كَم|ACC'),
    (1, r'INTG(\tSTEM\|POS:)INTG(\|LEM:كَم)', r'N\1N\2|ACC'),
    (1, r'(2:249:49|53:26:1)(.*)LEM:كَم\|ACC', r'\1\2LEM:كَم|NOM'),
    (1, r'(2:211:4|2:259:24|18:19:8|23:112:2)(.*)N\tSTEM\|POS:N', r'\1\2INTG\tSTEM|POS:INTG'),

    # أي fixes
    # أيها or أيتها: fix LEM
    (1, r'LEM:أَيّ(َت)?ُهَا\|NOM', 'LEM:أَيُّهَا|ACC'),
    (1, r'(LEM:أَيُّهَا|LEM:أَىّ)(\|?)', r'\1|ROOT:أيي\2'),
    (0, 'LEM:أَىّ|', 'LEM:أَيّ|'),
    (1, r'(28:28:5:1.*)', r'\1|ACC'),
    (1, r'(18:12:4:1.*)', r'\1|NOM'),
    (1, r'(17:110:7:1|82:8:2:1)(.*?)N(.*:)N(.*)', r'\1\2COND\3COND\4'),
    (1, r'(17:110:8:1)(.*?)REL(.*:)REL(.*)', r'\1\2SUP\3SUP\4'),
    (1, r'(82:8:4:1)(.*?)REL(.*:)REL(.*)', r'\1\2SUP\3SUP\4'),
    (1, r'(18:19:28:1)(.*?)N(.*:)N(.*)ُهَا(.*)ACC', r'\1\2INTG\3INTG\4\5NOM'),
    (1, r'(40:81:3:2)(.*?)N(.*:)N(.*)\|NOM', r'\1\2INTG\3INTG\4|ACC'),
    (1, r'(19:69:6:1.*)INTG(.*)INTG.*', r'\1REL\2REL|LEM:أَيّ|ROOT:أيي|ACC'),
    # أي: N -> INTG
    (1, r'^(7:185:19:3|31:34:21:2|45:6:7:3|53:55:1:3|55:13:1:3|55:16:1:3|55:18:1:3|55:21:1:3|55:23:1:3|55:34:1:3|55:38:1:3|55:45:1:3|55:47:1:3|55:51:1:3|55:53:1:3|55:55:1:3|55:73:1:3|55:75:1:3|55:77:1:3|67:2:6:1|77:12:1:2)(.*?)N(.*:)N(.*)', r'\1\2INTG\3INTG\4'),

    # أيها: mark the trailing هَا as ATT
    (1, r'^([\d:]+):2\t(.*?)(هَا?)(\tN\tSTEM\|POS:N\|LEM:أَيّ)ُهَا(.*)', r'\1:2\t\2\4\5\n\1:3\t\3\tATT\tSUFFIX|هَ+'),
    (1, r'^([\d:]+):1\t(.*?)(هَا?)(\tN\tSTEM\|POS:N\|LEM:أَيّ)ُهَا(.*)', r'\1:1\t\2\4\5\n\1:2\t\3\tATT\tSUFFIX|هَ+'),

    # أَيَّانَ to INTG
    (1, r'(79:42:4:1)(.*?)T(.*:)T(.*)', r'\1\2INTG\3INTG\4'),

    # إذا fixes
    (1, r'(ًا\t)SUR(\tSTEM\|POS:)SUR', r'\1ANS\2ANS'),
    (1, r'^(9:58:14:1|16:4:5:2|16:54:6:1|21:12:4:1|21:18:7:2|21:97:4:2|23:64:6:1|24:48:8:1|26:32:3:2|27:45:10:2|28:18:6:2|30:20:8:1|30:33:14:1|30:48:26:1|36:37:7:2|36:51:4:2|36:77:8:2|37:19:5:2|39:45:16:1|39:68:19:2|41:34:10:2|43:47:4:1|43:57:6:1)(.*?)(T.*)', r'\1\2SUR\tSTEM|POS:SUR|LEM:إِذَا'),
    # إذا carries the meaning of COND, but not its behavior (لا يجزم إلا في الشعر)
    (1, r'(.*إِذَا\t)COND(.*)COND(.*)', r'\1T\2T\3'),

    # Grammar fix ("أعظم" خبر, وليس نعتا)
    (1, r'(9:20:10:1.*)ADJ\|(.*)', r'\1\2'),
    # موسى: منادى مرفوع
    (1, r'(\tيَٰ\t.*\n.*مُوسَىٰ\|M\|)ACC', r'\1NOM'),

    # حيث is LOC
    (1, r'N(\tSTEM\|POS:)N(\|LEM:حَيْث\|ROOT:حيث\|GEN)', r'LOC\1LOC\2'),

    # أما حرف تفصيل ويضمن معنى الشرط
    (1, r'COND(.*)COND(\|LEM:أَمَّا)', r'EXL\1EXL\2'),

    # إما EXL -> COND
    (1, r'^(10:46:1:2|17:23:9:1|17:28:1:2|19:26:5:2|23:93:3:1|40:77:6:2|41:36:1:2|43:41:1:2)(.*?)EXL(.*?)EXL(.*?)', r'\1\2COND\3COND\4'),

    # أنى: remove root, mark as INTG
    (1, r'LEM:أَنَّىٰ\|ROOT:أني(\|ACC)?', 'LEM:أَنَّىٰ|ACC'),
    (0, 'أَنَّىٰ\tN\tSTEM|POS:N', 'أَنَّىٰ\tINTG\tSTEM|POS:INTG'),

    # أين is always LOC-INTG, mark as LOC for consistency
    (1, r'^(57:4:30:1|58:7:34:1)(.*?)INTG(.*?)INTG(.*?)', r'\1\2LOC\3LOC\4'),

    # Split إِلَّمْ
    (0, '11:14:1:2\tإِلَّمْ\tCOND\tSTEM|POS:COND|LEM:إِلَّم', '11:14:1:2\tإِ\tCOND\tSTEM|POS:COND|LEM:إِن\n11:14:1:3\tلَّمْ\tNEG\tSTEM|POS:NEG|LEM:لَم'),

    # Fix lemma of لما
    (1, r'(لّ?َمَّا\tNEG\tSTEM\|POS:NEG\|LEM:لَم)$', r'\1َّا'),
    # لَمَّا استثنائية
    (1, r'(36:32:3:1.*?)T(.*:)T(.*)', r'\1EXP\2EXP\3'),
    # لما occurrence: T > NEG
    (1, r'(3:142:6:2\tلَمَّا\t)T(\tSTEM\|POS:)T(\|LEM:لَمَّا)', r'\1NEG\2NEG\3'),

    # أسماء الإشارة fixes
    # أُولَآء: return to P
    (1, r'(LEM:أُولَآء\|)2?MP', r'\1P'),
    # Return all LEMS to ذا
    (1, r'(LEM:)(هَٰذَا|هَٰذَٰن|ذَٰنِك|ذَٰلِك|تِلْكُم|هَٰتَيْن|هَٰكَذَا|أُولَٰٓئِك|أُولَآء)', r'\1ذَا'),
    # هَٰ: separate and mark as ATT
    (1, r'^(.*:)(\d)(\tهَٰٓ?)(.*LEM:ذَا.*)', lambda m: m.expand(r'\1\2\3\tATT\tPREFIX|هَ+\n\1') + str(int(m.group(2))+1) + '\t' + m.group(4)),
    # ل: seperate and mark as distance, ك(ما/م/ن): seperate and mark as مخاطب
    (1, r'(.*:)(\d)(\t.+?)(ل[ِْ])?(ك.+)(\t.*\t.*LEM:(?:ذَا|هُنَا).*)', split_dem),
    # كَذَا: (ك) للتشبيه
    (1, r'(27:42:4):3(\tكَ)(.*)', r'\1:3\2\tP\tPREFIX|كَ+\n\1:4\t\3|MS'),
    # ذا: return to MS
    (1, r'(ذَٰ\t.*LEM:ذَا\|)(?!MS)(.*)', r'\1MS'),

    # 3 DEMs are RELs
    (1, r'(.*)REL(.*)REL(\|LEM:ذَا.*)', r'\1DEM\2DEM\3'),
    # هُنَالِكَ is all LOC-DEM
    (1, r'(.*هُنَالِكَ\t)(T|LOC)(.*)(T|LOC)(.*:هُنَا)لِك', r'\1DEM\3DEM\5'),

    # إن شرطية إلى نافية
    (1, r'(26:113:1:1|36:32:1:2)(.*?)COND(.*:)COND(.*)', r'\1\2NEG\3NEG\4'),
    # إن شرطية إلى توكيد
    (1, r'(26:97:2:1|26:186:6:2|28:10:6:1|30:49:1:2)(.*?)COND(.*:)COND(.*)', r'\1\2CERT\3CERT\4'),

    # كيف from INTG to N
    (1, r'^(2:259:52|2:260:6|3:6:6|4:50:2|6:24:2|6:46:18|6:65:23|7:84:5|7:86:21|7:103:13|7:129:21|10:39:16|10:73:14|12:109:17|14:24:3|14:45:9|16:36:25|17:21:2|17:48:2|25:9:2|25:45:5|27:14:8|27:51:2|27:69:6|28:40:7|29:19:3|29:20:6|30:9:6|30:42:6|30:48:10|30:50:6|35:44:6|37:73:2|40:21:6|40:82:6|43:25:4|47:10:6|50:6:6|67:17:11|71:15:3|74:19:2|74:20:3|88:17:5|88:18:3|88:19:3|88:20:3|89:6:3|105:1:3|6:11:7|10:14:9)(.*?)INTG(.*:)INTG(.*)', r'\1\2N\3N\4'),

    # ما شرطية إلى موصول
    (1, r'(13:17:33:1)(.*?)COND(.*:)COND(.*)', r'\1\2REL\3REL\4'),
    # لو شرطية إلى لو مصدرية
    (1, r'^(15:2:5:1|33:20:9:1)(.*?)COND(.*:)COND(.*)', r'\1\2SUB\3SUB\4'),
    # لو مصدرية إلى لو شرطية
    (1, r'^(2:170:15:3|2:221:11:2|2:221:23:2|5:100:6:2|59:9:21:2|75:15:1:2)(.*?)SUB(.*:)SUB(.*)', r'\1\2COND\3COND\4'),

    # أين مكانية إلى شرطية
    (1, r'^(3:112:4:1|16:76:15:1|19:31:3:1|33:61:2:1)(.*)LOC(.*:)LOC(.*)', r'\1\2COND\3COND\4'),

    # أسماء الأفعال
    # مساس: اسم، لا اسم فعل
    (1, r'(20:97:10:1)(.*?)IMP(.*:)IMP(.*)', r'\1\2\3\4|ACC'),
    # هَآؤُم
    (1, r'(69:19:7:1.*)IMPN(.*)IMPN(.*)', r'\1NV\2NV|IMPV\3|ROOT:هاء'),
    # هلم
    (1, r'(.*\tهَ).*\n.*?(لُمَّ\t)V(.*?)V(.*)\|\(I\)(\|LEM:).*?(\|ROOT:).*?(\|.*)', r'\1\2NV\3NV\4\5هَلُمّ\6هلم\7'),
    # أف
    (1, r'(أُفٍّ\t)N(.*:)N(.*)\|INDEF.*', r'\1NV\2NV|IMPF\3'),
    # هيهات
    (1, r'(هَيْهَاتَ\t)N(.*:)N(.*)\|ACC.*', r'\1NV\2NV|PERF\3'),
    # هيت
    (1, r'(هَيْتَ\t)V(.*:)V(\|IMPV.*)', r'\1NV\2NV\3'),
    # عليكم
    (1, r'(5:105:4:1.*?)P(.*:)P(.*)', r'\1NV\2NV|IMPV\3'),
    # مكانكم
    (1, r'(10:28:8:1.*?)N(.*:)N(.*)', r'\1NV\2NV|IMPV\3'),
    # وي كأن
    (1, r'(.*):(\d)(\tوَيْ)(كَأَنَّ.*)(وَيْ)(كَأَنّ.*)', r'\1:\2\3\tNV\tSTEM|POS:NV|IMPF|LEM:\5\n\1:2\t\4\6'),
    (1, r'(28:82:23):2(\tهُۥ)', r'\1:3\2'),

    # دَعَانِ (2:186:11:1): fix
    (1, r'(2:186:11:1.*)(\tV.*)IMPV(.*2M)D(\n[\d:]+).*\n(?:[\d:]+)(.*\n)', r'\1ا\2PERF\3S\4\5'),

    # هنيئا, مريئا: remove ADJ
    (1, r'ADJ\|(LEM:هَنِيٓـٔ|LEM:مَرِيٓـٔ)', r'\1'),

    # ليالي ظرف زمان
    (1, r'(34:18:15:1.*)N(.*)N(.*)', r'\1T\2T\3'),

    # Fix gender and grammatical person
    (1, r'(33:48:2:1.*2)F(S.*)', r'\1M\2'),
    (1, r'(55:50:3:1.*)\|2(FD)', r'\1|3\2'),

    # Lemma spelling fixes
    # Remove madds
    (1, r'(LEM:[^|\n]+)ٓ', r'\1'),
    # Standardize hamzas
    (0, 'LEM:نَـَٔا', 'LEM:نَأَى'), # Edge case
    (1, r'(LEM:[^|\n]+[^ِ])ـَٔا', r'\1آ'),
    (1, r'(LEM:[^|\n]+ْ)ـٔ\|', r'\1ء|'),
    (0, 'LEM:مَسْـُٔول', 'LEM:مَسْئُول'),        # Edge case
    (0, 'LEM:اسْتَيْـَٔسَ', 'LEM:اسْتَيْأَسَ'),  # Edge case
    (1, r'(LEM:[^|\n]+[^ي][^يِ])ـٔ(?!ِ)', r'\1أ'),  # Inverse of: (ِـ|ي.?ـ|ـِٔ)
    (1, r'(LEM:[^|\n]+)ـٔ', r'\1ئ'),

    # General tag modifications
    # Mark verb forms using Arabic numerals
    (1, r'\(([IVX]+)\)', lambda m: 'VF:' + str(verb_forms.index(m.group(1)) + 1)),
    # Remove superflous STEM & POS tag
    (1, r'STEM\|POS:[^|\n]+\|?', ''),
    # Move PASS after VF
    (1, r'(PASS\|)(VF:[^|\n]+\|)', r'\2\1'),
    # Move ADJ to end
    (1, r'(ADJ)\|(.*$)', r'\2|\1'),
    # Move ROOT before LEM
    (1, r'(LEM:[^|\n]+)\|(ROOT:[^|\n]+)', r'\2|\1'),
]

f = 'quranic-corpus-morphology-0.4-ar.txt'
text = io.open(f).read()
for fix in fixes:
    print 'Replacing ', fix[1]
    if fix[0]:
        text = re.sub(fix[1], fix[2], text, flags=re.M)
    else:
        text = text.replace(fix[1], fix[2])
io.open(f, 'w', encoding='utf-8').write(text)
