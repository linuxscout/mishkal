# -*- coding=utf-8 -*-
CorrectedTashkeel = {
    # Original corrections
    u"قال:": u'قَالَ:',
    u"ثم": u'ثُمَّ',
    u'ثنا': u'ثَنَا',

    # Common function words written without hamza.
    # These unambiguous forms are not valid Arabic words otherwise,
    # so pre-correcting them is safe and prevents the morphological
    # analyzer from misidentifying them.
    # الى (without hamza) has no valid alternative reading
    u'الى': u'إِلَى',
    # أيضا is unambiguous (only one reading with fathatan)
    u'أيضا': u'أَيْضًا',
}
