from anki.hooks import addHook
from aqt import mw
from aqt.utils import showInfo
import pprint

# from .behavior import update_fields
from .main import config


class EditManager:
    def __init__(self):
        addHook('setupEditorButtons', self.setupButton)
        addHook('loadNote', self.updateButton)
        addHook('editFocusLost', self.onFocusLost)

    def setupButton(self, buttons, editor):
        self.editor = editor
        self.buttonOn = False
        editor._links['formatExamples'] = self.onToggle

        button = editor.addButton(
            icon=None,
            cmd='formatExamples',
            tip='Format examples',
            label='<b>Test!</b>',
            func=self.onToggle,
            id='formatExamples',
            toggleable=True,
        keys="Ctrl+;")

        return buttons + [button]

    def onToggle(self, editor):
        self.buttonOn = not self.buttonOn

        mid = str(editor.note.model()['id'])

        # if self.buttonOn and mid not in config['enabledModels']:
        #     config['enabledModels'].append(mid)
        # elif not self.buttonOn and mid in config['enabledModels']:
        #     config['enabledModels'].remove(mid)
        print('Clicked!')
        showInfo(f'Note: {pprint.pformat(editor.note.items())}')
        # showInfo("Card count: %d" % 123)

        config.save()

    def updateButton(self, editor):
        enabled = str(editor.note.model()['id']) in config['enabledModels']

        if (enabled and not self.buttonOn) or (not enabled and self.buttonOn):
            editor.web.eval('toggleEditorButton(formatExamples);')
            self.buttonOn = not self.buttonOn

    def onFocusLost(self, _, note, index):
        if not self.buttonOn:
            return False

        allFields = mw.col.models.fieldNames(note.model())
        field = allFields[index]

        # if update_fields(note, field, allFields):
        #     if index == len(allFields) - 1:
        #         self.editor.loadNote(focusTo=index)
        #     else:
        #         self.editor.loadNote(focusTo=index+1)

        return False


def append_tone_styling(editor):
    js = 'var css = document.styleSheets[0];'

    for line in editor.note.model()['css'].split('\n'):
        if line.startswith('.tone'):
            js += 'css.insertRule("{}", css.cssRules.length);'.format(
                line.rstrip())

    editor.web.eval(js)