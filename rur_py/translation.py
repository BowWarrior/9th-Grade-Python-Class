# -*- coding: latin-1 -*-

""" RUR-PLE: Roberge's Used Robot - a Python Learning Environment
    translation.py
    Version 1.0
    Author: Andre Roberge    Copyright  2006
    andre.roberge@gmail.com
"""

# This file can be modified to add translations to other languages.
# A "basic but complete" translation includes TWO files:
#  - a ".po" file, added in the proper directory (folder)
#  - a "rur.htm" file, also added in the proper directory (folder); this file
#    is the one displayed in the browser.  Ideally, this last folder should
#    also contain a translation of all the lessons! :-)  At the very least,
#    make a copy of an existing rur.htm file (e.g. the English one) and put
#    it in the appropriate folder.
#
#  For example, let HOME be the directory in which RUR_start.py is located.
#  The English .po file is located at HOME/rur_locale/en/english.po
#  and the English rur.htm file is located at HOME/lessons/en/rur.htm.

# wxPython comes in two basic "versions" (ansi and unicode). The recommended
# version is the unicode one; the following code, which has only been tested
# with earlier versions of rur-ple (circa 2005)
# should deal properly with the ansi version of wxPython.
import wx
def my_unicode(str):
    return str
def my_ansi(str):
    return str.encode('utf-8')
if "unicode" in wx.PlatformInfo:
    my_encode = my_unicode
else:
    my_encode = my_ansi

import os
import misc # needed for the locating rur-ple's home directory

# You can add a new language in the following dict.
# The first entry is the name of the language as you want it to appear in
# the menu;
# the second is simply an empty dict which will be filled with translation
# values when needed;
# the third is the language code (also the sub-directory name);
# the fourth is the name of the ".po" file, assumed to be utf-8 encoded.
languages = {
    'english': [my_encode('English'), {}, 'en', 'english.po'],
    'french': [my_encode(u'Fran�ais'), {}, 'fr', 'french.po'],
    'german': [my_encode(u'Deutsch'), {}, 'de', 'german.po'],
    'spanish': [my_encode(u'Espa�ol'), {}, 'es', 'spanish.po'],
    'turkish': [my_encode(u'T�rk�e'), {}, 'tr', 'turkish.po'],
    'welsh': [my_encode('Welsh'), {}, 'cy', 'welsh.po']
}

#============
#
# You should not need to modify any of the following.

# Note: the base directory is called "rur_locale" instead of "locale".
# If a directory named "locale" exists, wxPython assumes it uses the
# standard 'gettext' approach and expects some standard functions to
# be defined - which they are not in my customized version.
language_code = 'en'
_selected = None

_user_dir = os.path.join(os.path.expanduser("~"), ".rurple")
if not os.path.exists(_user_dir):  # first time ever
    try:
        os.makedirs(_user_dir)
    except:
        print "Could not create the user directory."
        _user_dir = None

_user_file = os.path.join(_user_dir, "rurple.lang")

def build_dict(filename):
    translation = {}
    """This function creates a Python dict from a simple standard .po file."""
    lines = open(filename).readlines()
    header = True
    msgid = False
    msgstr = False
    for line in lines:
        line = line.decode("utf-8") # encoding that was generated by poedit;
        if header:       # may need to be adapted to extract the information
            if line.startswith("#"): header = False # from the .po file
        else:
            if line.startswith("msgid "):
                msgid = True
                key = line[7:-2]  # strips extra quotes and newline character
                                  # as well as the "msgid " identifier
            elif line.startswith("msgstr "):
                msgstr = True
                msgid = False
                value = line[8:-2]
            elif line.startswith('"') or line.startswith("'"):
                if msgid:
                    key += line[1:-2]
                elif msgstr:
                    value += line[1:-2]
            elif line.startswith("\n"):
                key = key.replace("\\n","")
                value = value.replace("\\n", "\n")
                translation[key] = value
                msgid = False
                msgstr = False
    return translation

rur_locale = os.path.join(misc.HOME, "rur_locale")
for lang in languages:
    filename = os.path.join(rur_locale, languages[lang][2], languages[lang][3])
    languages[lang][1] = build_dict(filename)

def _select_code(lang_code):
    global _selected, _changed, language_code
    for lang in languages:
        if languages[lang][2] == lang_code:
            _selected = languages[lang][1]
            language_code = lang_code
            _save_language(lang_code)

def select(language):
    for lang in languages:
        if language == languages[lang][0]:
            _select_code(languages[lang][2])

def _(message):
    global _selected
    if _selected is None:
        _selected = 'en'
    key = message.replace("\n","")  # message is a key in a dict
    if key in _selected:
        return _selected[key]
    else:
        return message

def _save_language(lang):
    try:
        f = open(_user_file, 'w')
        f.write(lang)
        f.close()
    except:
        print "Could not save language preference"
        print "lang = ", lang
        print "_user_file = ", _user_file
        pass

def _load_default():
    global language_code
    try:
        lang = open(_user_file, 'r').read()
    except:
        print "Language preference not found; default to English."
        lang = 'en'
    _select_code(lang)

_load_default()  # import the default language at the start