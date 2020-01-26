BASEPATH = './res/fonts/'

# Most lang codes conform to ISO 639-1;
# however, the author thinks practicality beats purity
# and adds a few non-ISO (noted) internal lang codes
# for users' convenience.
# When a new language is introduced but the ISO code of
# the new lang conflicts with one of the existent, non-ISO ones,
# the non-ISO lang code is removed and replaced with the new one
# with notice.
__langs__ = [
    # originally intended audience
    ('en', 'NotoSans-Regular.ttf'),
    # the "kinda expected" zone
    # CJK, any Noto CJK font supports all three languages
    # both SC and TC, JP, KR.
    ('zh', 'NotoSansCJKsc-Regular.otf'),
    ('ja', 'NotoSansCJKsc-Regular.otf'),
    ('jp', 'NotoSansCJKsc-Regular.otf'),  # non-ISO
    ('ko', 'NotoSansCJKsc-Regular.otf'),
    ('kr', 'NotoSansCJKsc-Regular.otf'),  # non-ISO
    # "HOW COULD I KNOW SOMEONE WOULD REQUEST
    # FOR A [INSERT LANGUAGE HERE] MEME"
    ('he', 'NotoSansHebrew-Regular.ttf')
]

LANGS = {}

for lang, font in __langs__:
    LANGS[lang] = BASEPATH + font

MONO = BASEPATH + 'NotoSansMono-Regular.ttf'