import re
import string
from aqt.utils import showInfo


row_template = string.Template('<td style="width: 33.3333%;">$text</td>')
def transformToHtmlTable(examples):
    content = '''<table style="border-collapse: collapse; width: 100%;" border="1">
<tbody>'''
    for example in examples:
        content += string.Template('''
        <tr>
            <td style="width: 33.3333%;">$chinese</td>
            <td style="width: 33.3333%;">$english</td>
            <td style="width: 33.3333%;">$pinyin</td>
        </tr>''').safe_substitute(example)
    content += '''
    </tbody>
    </table>'''
    return content


def format_english(hanzi, original_examples, silhouette, pinyin):
    # parsed = parse_row(original_examples)
    # if parsed is None:
    #     print(rf'Bad formatting? Hanzi: {hanzi} Original examples: ' + original_examples)
    #     return None
    original_examples_list = [example.split('|') for example in original_examples.split('<br>')]
    original_examples_list = [[subpart.replace('<div>', '').replace('</div>', '').replace('&nbsp;', '').rstrip() for subpart in example] for example in original_examples_list]
    filtered_examples = [example for example in original_examples_list if len(example) == 3]
    bad_examples = [example for example in original_examples_list if len(example) != 3]
    showInfo(f'Bad examples?: {bad_examples}')
    # showInfo(pprint.pformat(filtered_examples), textFormat='plain')
    filtered_dict = [{'chinese': example[0], 'pinyin': example[1], 'english': example[2]} for example in filtered_examples]
    # showInfo(pprint.pformat(filtered_dict))
    finished_examples = transformToHtmlTable(filtered_dict)
    # print(finished_examples)
    finished_examples = finished_examples.replace('\n', '')
    return finished_examples, convert_front_examples(finished_examples, hanzi, silhouette, pinyin)

strip_html_regex = re.compile(r'<[A-Za-z\s=\"\d]+>(.*?)<\/\w+>')
def convert_front_examples(examples, hanzi, raw_silhouette, raw_pinyin):
    new_pinyin = ''.join(strip_html_regex.findall(raw_pinyin))
    # showInfo(f'{raw_pinyin}\n\n new: {new_pinyin}', textFormat='plain')

    modified_silhouette = ' ' + raw_silhouette + ' '
    example_front = examples.replace(hanzi.rstrip(), modified_silhouette)
    pinyin_regex = re.compile(re.escape(new_pinyin.strip()), re.IGNORECASE)
    example_front_2 = pinyin_regex.sub(raw_silhouette, example_front)
    # example_front_2 = re.compile(new_pinyin).sub(row['Silhouette'], example_front)
    return example_front_2