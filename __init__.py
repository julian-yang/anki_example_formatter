from . import test
# from .config import ConfigManager
# config = ConfigManager()
# test.EditManager()
import pprint
import webbrowser

# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, openLink
# import all of the Qt GUI library
from aqt.qt import *
from anki.hooks import addHook
import sys
from .lib.pinyin import pinyin
from os.path import dirname, join

sys.path.append(join(dirname(__file__), 'lib'))


# input: the text from "Examples" field, this should be a list of example sentences.
# returns: html table properly formatted.
def format_examples(examples):
    print('hello')

def find_examples(editor):
    if 'Hanzi' not in editor.note.keys():
        showInfo(f"couldn't find Hanzi field! note fields: {editor.note.keys}")
        return
    hanzi = editor.note['Hanzi']
    examples_link = f'https://tw.ichacha.net/zaoju/{hanzi}.html'
    openLink(examples_link)

def onToggle(editor):
    mid = str(editor.note.model()['id'])

    # if self.buttonOn and mid not in config['enabledModels']:
    #     config['enabledModels'].append(mid)
    # elif not self.buttonOn and mid in config['enabledModels']:
    #     config['enabledModels'].remove(mid)
    print('Clicked!')
    if 'Hanzi' not in editor.note.keys() or 'Examples' not in editor.note.keys():
        showInfo(f"couldn't find field! note fields: {editor.note.keys}")
        return
    hanzi = editor.note['Hanzi']
    # examples_link = f'https://tw.ichacha.net/zaoju/{hanzi}.html'
    # openLink(examples_link)
    # showInfo(f'<a href=\"{examples_link}\">{examples_link}</a>', textFormat='rich')

    examples = editor.note['Examples']
    # showInfo(f'Hanzi: {hanzi}\nExamples:{pprint.pformat(examples)}')
    editor.note['Examples-front'] = 'hello world!'
    editor.note.flush()
    editor.setNote(editor.note)


def setupButton(buttons, editor):
    editor._links['formatExamples'] = onToggle
    # showInfo(f'Buttons: {pprint.pformat(buttons)}')

    button = editor.addButton(
        icon=None,
        cmd='formatExamples',
        tip='Format examples',
        label='<b>Test!</b>',
        func=onToggle,
        id='formatExamples',
        toggleable=True,
        keys="Ctrl+;")

    find_examples_button = editor.addButton(
        icon=None,
        cmd='findExamples',
        tip='Find Examples',
        label='<b>Find Examples</b>',
        func=find_examples,
        id='findExamples',
        toggleable=True,
        keys="Ctrl+/")

    return buttons + [button, find_examples_button]

addHook('setupEditorButtons', setupButton)

