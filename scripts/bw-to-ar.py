# -*- coding: utf-8
from __future__ import unicode_literals
import io
import re
"""
Returns Buckwalter transliteration present in
quranic-corpus-morphology-0.4.txt to Arabic.

See: https://github.com/mustafa0x/quran-morphology
"""

bw = {
    "'":'ء', '>':'أ', '&':'ؤ', '<':'إ', '}':'ئ', 'A':'ا', 'b':'ب',
    'p':'ة', 't':'ت', 'v':'ث', 'j':'ج', 'H':'ح', 'x':'خ', 'd':'د',
    '*':'ذ', 'r':'ر', 'z':'ز', 's':'س', '$':'ش', 'S':'ص', 'D':'ض',
    'T':'ط', 'Z':'ظ', 'E':'ع', 'g':'غ', '_':'ـ', 'f':'ف', 'q':'ق',
    'k':'ك', 'l':'ل', 'm':'م', 'n':'ن', 'h':'ه', 'w':'و', 'Y':'ى',
    'y':'ي', 'F':'ً', 'N':'ٌ', 'K':'ٍ', 'a':'َ', 'u':'ُ', 'i':'ِ',
    '~':'ّ', 'o':'ْ', '^':'ٓ', '#':'ٔ', '`':'ٰ', '{':'ٱ', ':':'ۜ',
    '@':'۟', '"':'۠', '[':'ۢ', ';':'ۣ', ',':'ۥ', '.':'ۦ', '!':'ۨ',
    '-':'۪', '+':'۫', '%':'۬', ']':'ۭ',
}
bw_map = { ord(k):bw[k] for k in bw }
trans = [
    r'(?<=ROOT:)([^|\n]+)',
    r'(?<=LEM:)([^|\n]+)',
    r'(?<=SP:)([^|\n]+)',
    r'(?<=PREFIX\||SUFFIX\|)(?!PRON)(?<=\+)?(.*?)(?=:|\+)'
]

lines = list(io.open('quranic-corpus-morphology-0.4.txt'))
out = io.open('quranic-corpus-morphology-0.4-ar.txt', 'w', encoding='utf-8')
out.write(''.join(lines[:57]))  # Add copyright blocks

for line in lines[57:]:
    parts = line.split('\t')
    parts[0] = parts[0][1:-1]  # Remove parans around surah:ayah:word:part
    parts[1] = parts[1].translate(bw_map)
    parts[3] = re.sub('|'.join(trans), lambda m: m.group(0).translate(bw_map), parts[3])
    out.write('\t'.join(parts))
