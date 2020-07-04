from . import test
# from .config import ConfigManager
# config = ConfigManager()
# test.EditManager()
import pprint

# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *
from anki.hooks import addHook


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
    examples = editor.note['Examples']
    showInfo(f'Hanzi: {hanzi}\nExamples:{pprint.pformat(examples)}')


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

    return buttons + [button]

addHook('setupEditorButtons', setupButton)

