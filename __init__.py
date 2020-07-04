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
import string



# call render with a dict containing: list of dict['chinese', 'pinyin', 'english']
# table_template = Template('''<table style="border-collapse: collapse; width: 100%;" border="1">
# <tbody>
# {% for example in examples -%}
# <tr>
# <td style="width: 33.3333%;">{{example.chinese}}</td>
# <td style="width: 33.3333%;">{{example.english}}</td>
# <td style="width: 33.3333%;">{{example.pinyin}}</td>
# </tr>
# {% endfor -%}
# </tbody>
# </table>
# ''')


def create_html_table(dict_examples):
    html_table = '''<table style="border-collapse: collapse; width: 100%;" border="1">
<tbody>\n'''
    for example_dict in dict_examples:
        html_table += string.Template('''
        <tr>
        <td style="width: 33.3333%;">$chinese</td>
        <td style="width: 33.3333%;">$english</td>
        <td style="width: 33.3333%;">$pinyin</td>
        </tr>
        ''').safe_substitute(example_dict)
    html_table += '''</tbody>
    </table>'''
    return html_table.replace('\n','')


# input: the text from "Examples" field, this should be a list of example sentences.
# returns: html table, front html table properly formatted.
def format_examples(html_examples, hanzi, silhouette):
    examples = html_examples.replace('<div>', '').replace('</div>', '').split('<br>')
    examples = [example for example in examples if example.rstrip()]
    examples = [example.split('|') for example in examples]
    # showInfo(f'before split: {html_examples}\n\nafter split: {pprint.pformat(examples)}', textFormat='plain')
    examples_dict = []
    front_examples_dict = []
    for example in examples:
        chinese_idx = 0
        english_idx = 0 if chinese_idx == 1 else 1
        chinese = example[chinese_idx]
        front_chinese = example[chinese_idx].replace(hanzi, f' {silhouette} ')
        examples_dict.append({'chinese': chinese, 'pinyin': pinyin.get(chinese), 'english': example[english_idx]})
        front_examples_dict.append({'chinese': front_chinese, 'pinyin': pinyin.get(front_chinese), 'english': example[english_idx]})
    return create_html_table(examples_dict), create_html_table(front_examples_dict)


def find_examples(editor):
    if 'Front' not in editor.note.keys():
        showInfo(f"couldn't find Front field! note fields: {editor.note.keys}")
        return
    hanzi = editor.note['Front']
    examples_link = f'https://tw.ichacha.net/zaoju/{hanzi}.html'
    examples_link = f'https://www.yellowbridge.com/chinese/sentsearch.php?word={hanzi}'
    # examples_link = f'https://tw.ichacha.net/search.aspx?q={hanzi}&l=en'
    openLink(examples_link)


def onToggle(editor):
    mid = str(editor.note.model()['id'])

    # if self.buttonOn and mid not in config['enabledModels']:
    #     config['enabledModels'].append(mid)
    # elif not self.buttonOn and mid in config['enabledModels']:
    #     config['enabledModels'].remove(mid)
    editor.note.flush()
    editor.note.load()
    print('Clicked!')
    if not all(key in editor.note.keys() for key in ['Front', 'Examples', 'Silhouette']):
        showInfo(f"couldn't find field! note fields: {editor.note.keys}")
        return
    hanzi = editor.note['Front']

    # examples_link = f'https://tw.ichacha.net/zaoju/{hanzi}.html'
    # openLink(examples_link)
    # showInfo(f'<a href=\"{examples_link}\">{examples_link}</a>', textFormat='rich')

    examples = editor.note['Examples']
    silhouette = editor.note['Silhouette']
    formatted_examples, front_formatted_examples = format_examples(examples, hanzi, silhouette)
    editor.note['Examples'] = formatted_examples
    editor.note.flush()
    editor.note['Examples-front'] = front_formatted_examples
    editor.note.flush()
    backend_note = mw.col.getNote(editor.note.id)

    editor.setNote(backend_note)
    showInfo(pprint.pformat(backend_note['Examples']))


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

