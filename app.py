'''
    Name: main.py
    Writer: Hoseop Lee, Ainizer
    Rule: Flask app
    update: 21.03.02
'''
# external module
from flask import Flask, request, render_template, send_file
from werkzeug.datastructures import ImmutableOrderedMultiDict       # 순서있는 리퀘스트 딕셔너리? 사용
from werkzeug.exceptions import RequestEntityTooLarge, BadRequestKeyError   # for file limit except
from werkzeug.utils import secure_filename      # file extension check
import contractions
import unidecode
from num2words import num2words
import emoji

# internal module
from threading import Thread
from queue import Queue, Empty
import time
import os
import io
import re

# 순서있는 걸로 변경
Flask.request_class.parameter_storage_class = ImmutableOrderedMultiDict

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024    # file upload limit 200mb
ALLOWED_EXTENSIONS = {'txt'}        # only support text file.

requests_queue = Queue()
BATCH_SIZE = 1
CHECK_INTERVAL = 0.1

DATA_FOLDER = './data'
UPLOAD_FOLDER = './data/upload'
RESULT_FOLDER = './data/result'


# create folder
if not os.path.isdir(DATA_FOLDER):
    os.mkdir(DATA_FOLDER)

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

if not os.path.isdir(RESULT_FOLDER):
    os.mkdir(RESULT_FOLDER)


def handle_requests_by_batch():
    while True:
        request_batch = []

        while not (len(request_batch) >= BATCH_SIZE):
            try:
                request_batch.append(
                    requests_queue.get(timeout=CHECK_INTERVAL))
            except Empty:
                continue

            for requests in request_batch:

                try:
                    requests["output"] = transform(
                        requests['input'][0], requests['input'][1])
                except Exception as e:
                    requests["output"] = e


handler = Thread(target=handle_requests_by_batch).start()


##
# String to capitalize
def to_capitalize(text):
    text = list(map(lambda x: x.capitalize(), text.split(". ")))

    result = ". ".join(text)

    return result


##
# String to lower
def to_lower(text):
    result = text.lower()

    return result


##
# remove accent
# à -> a
def accent(text):
    result = unidecode.unidecode(text)

    return result


##
# Expand the abbreviation.
# ex) can't => can not
def expander(text):

    result = contractions.fix(text)

    return result


##
# short string remover
def short_line_remover(text, size):
    if len(text) <= int(size):
        text = ''

    return text


##
# short word remover
def short_word_remover(text, size):
    rule = r'\W*\b\w{1,' + str(size) + r'}\b'
    shortword = re.compile(rule)

    result = shortword.sub('', text)

    return result


##
# emoji remover
def emoji_remover(text):
    result = re.sub(emoji.get_emoji_regexp(), r"", text)

    return result


##
# emoji to text
def emoji_to_text(text):
    result = emoji.demojize(text, delimiters=(" ", ""))

    return result


##
# special character remover
def special_remover(text, special):
    special = '[' + special + ']'

    result = re.sub(special, " ", text)

    return result


##
# special character replacer
def special_replacer(text, specials, new):
    text: str

    for special in specials:
        text = text.replace(special, new)

    return text


##
# word replacer
def word_replacer(text, word, new):
    text: str

    text = text.replace(word, new)

    return text


def url_remover(text):
    result = re.sub(r"http\S+", "", text)

    return result


##
# Reduce whitespace to one
# ex) Hello,    guy -> Hello, guy
def space_normalizer(text):
    result = " ".join(text.split())

    if result == "":
        return result

    return result + " "


##
# normalize full stop
# ex) This is Kim; And me. -> This is Kim. And me.
def full_stop_normalizer(text, stops):
    text: str
    stops = '[' + stops + ']'

    result = re.sub(stops, ".", text)

    return result


##
# normalize comma
# ex) This is Kim: and he is my son. -> This is Kim, and he is my son.
def comma_normalizer(text, stops):
    text: str
    stops = '[' + stops + ']'

    result = re.sub(stops, ",", text)

    return result


##
# Change number to same text.
# ex) He is 3 years-old. -> He is three years-old.
def number_to_text(text):
    result = re.sub(r'\d+', lambda n: num2words(int(n.group())), text)

    return result


##
# number to word
# ex) if number == 1) He is 3 years-old. -> He is 1 years-old.
def number_normalizer(text, number):
    result = re.sub(r'\d+', number, text)

    return result


##
# html tag remove
def html_tag_remover(text):
    cleaner = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    result = re.sub(cleaner, '', text)
    return result


##
# file check
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


##
# text read and pre-processing
def transform(file, options):
    filename = secure_filename(file.filename)

    # Only receive text file.
    if not allowed_file(filename):
        return {'error': 'Please upload a text file.'}, 500

    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    result_path = os.path.join(RESULT_FOLDER, filename)

    try:
        with open(input_path, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
            with open(result_path, 'w', encoding='utf-8') as r:
                for line in lines:
                    for option in options:
                        option_name = option[0]
                        value = option[1]
                        value2 = option[2]

                        if option_name == "to_capitalize":
                            line = to_capitalize(line)
                        elif option_name == "to_lower":
                            line = to_lower(line)
                        elif option_name == "accent":
                            line = accent(line)
                        elif option_name == "expander":
                            line = expander(line)
                        elif option_name == "short_line_remover":
                            line = short_line_remover(line, value)
                        elif option_name == "short_word_remover":
                            line = short_word_remover(line, value)
                        elif option_name == "emoji_remover":
                            line = emoji_remover(line)
                        elif option_name == "emoji_to_text":
                            line = emoji_to_text(line)
                        elif option_name == "special_remover":
                            line = special_remover(line, value)
                        elif option_name == "special_replacer":
                            line = special_replacer(line, value, value2)
                        elif option_name == "space_normalizer":
                            line = space_normalizer(line)
                        elif option_name == "full_stop_normalizer":
                            line = full_stop_normalizer(line, value)
                        elif option_name == "comma_normalizer":
                            line = comma_normalizer(line, value)
                        elif option_name == "number_to_text":
                            line = number_to_text(line)
                        elif option_name == "number_normalizer":
                            line = number_normalizer(line, value)
                        elif option_name == "word_replacer":
                            line = word_replacer(line, value, value2)
                        elif option_name == "html_tag_remover":
                            line = html_tag_remover(line)
                        elif option_name == "url_remover":
                            line = url_remover(line)
                    r.write(line)

    except Exception as e:
        print('Error occur in pre-processing!', e)
        os.remove(input_path)
        os.remove(result_path)
        return {'error': 'Error occur in pre-processing!'}, 500

    with open(result_path, 'rb') as r:
        data = r.read()

    os.remove(input_path)
    os.remove(result_path)

    return io.BytesIO(data), filename, 200


def option_transform(options):
    options = options.split(",")

    return options


@app.route('/dpp', methods=['POST'])
def processor():
    try:
        if requests_queue.qsize() > BATCH_SIZE:
            return {'Error': 'Too Many Requests'}, 429

        args = []

        text_file = request.files['text_file']

        option_names = request.form.getlist('option')
        values = request.form.getlist('value')
        values2 = request.form.getlist('value2')

        options = list(zip(option_names, values, values2))

        args.append(text_file)
        args.append(options)

    except RequestEntityTooLarge as r:
        print(r)
        return {'error': 'The file size is too big!! It must be less then 200MB.'}, 413
    except BadRequestKeyError as b:
        return {'error': 'Bad request error. Try again.'}, 400
    except Exception as e:
        return {'error': e}, 421

    req = {"input": args}
    requests_queue.put(req)

    while 'output' not in req:
        time.sleep(CHECK_INTERVAL)

    result = req['output']

    if len(result) == 3:
        return send_file(result[0], mimetype='text/plain', attachment_filename=result[1]), result[2]
    else:
        return result


@app.route('/sample_download')
def send_csv_sample():
    return send_file('sample/test.txt', mimetype='text/plain', attachment_filename='sample.txt'), 200


@app.route('/healthz', methods=["GET"])
def health_check():
    return "Health", 200


@app.route('/')
def main():
    return render_template('app.html'), 200


if __name__ == '__main__':
    from waitress import serve
    serve(app, port=80, host='0.0.0.0')
