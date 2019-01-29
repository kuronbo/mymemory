import re

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from jinja2 import evalcontextfilter, Markup, escape

from application.category_solver import Category
from checkio_taker import service as checkio_s
from memoplat import service as memopla_s
from m_covers import service as mcovers_s


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

CATEGORY = Category()
app = create_app()


@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = '\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') \
                          for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


@app.route('/')
def index():
    responses = memopla_s.read_some_memo(page=0, page_size=10)
    return render_template('index.html', responses=responses[:9], category=CATEGORY,
                           q='',
                           page=0, has_next=len(responses)==10)


@app.route('/search')
def search():
    q = request.args.get('q')
    page = int(request.args.get('page', 0))
    if q:
        responses = memopla_s.read_some_memo_like_title(q, page=page, page_size=10)
    else:
        responses = memopla_s.read_some_memo(page=page, page_size=10)
    return render_template('search.html', responses=responses[:9], category=CATEGORY,
                           q='',
                           page=page, has_next=len(responses)==10)


@app.route('/m_cover/detail/<id>')
def cover_detail(id):
    memo = memopla_s.read_one_memo_eq_id(id)
    cover = mcovers_s.request_cover_by_id(id)
    return render_template('m_cover_detail.html', cover=cover, memo=memo)


@app.route('/m_cover/record', methods=['GET', 'POST'])
def record_cover():
    if request.method == 'GET':
        return render_template('m_cover_record.html')
    else:
        isbn = request.form['isbn']
        impression = request.form['impression']
        tagnames = request.form.getlist('tag')
        m_cover_command = mcovers_s.create_cover(isbn, impression)
        m_cover_command.flush()
        cover_values = m_cover_command.values_recorded(['id', 'title', 'caption'])
        memopla_command = memopla_s.create_memo(cover_values['id'],
                                                'm_cover',
                                                cover_values['title'],
                                                cover_values['caption'],
                                                tagnames=tagnames)
        memopla_command.flush()

        m_cover_command.commit()
        memopla_command.commit()
        return redirect(url_for('index'))


@app.route('/m_checkio/detail/<id>')
def detail_checkio(id):
    memo = memopla_s.read_one_memo_eq_id(id)
    problem = checkio_s.Request().by_id(id)
    return render_template('m_checkio_detail.html', memo=memo,
                           problem=problem)


@app.route('/m_checkio/record', methods=['POST', 'GET'])
def record_checkio():
    if request.method == 'GET':
        return render_template('m_checkio_record.html')
    else:
        island = request.form['island']
        title = request.form['title']
        level = int(request.form['level'])
        description = request.form['description']
        tagnames = request.form.getlist('tag')
        answers = []
        for who, code, imp in zip(request.form.getlist('answer_who'),
                                  request.form.getlist('answer_source_code'),
                                  request.form.getlist('answer_impression')):
            answers.append([who, code, imp])
        checkio_command = checkio_s.ProblemOperator()
        checkio_command.new(island=island, title=title, level=level, description=description)
        for answer in answers:
            checkio_command.add_answer(who=answer[0], source_code=answer[1], impression=answer[2])
        checkio_command.flush()
        response = checkio_command.property()

        memopla_command = memopla_s.create_memo(response['id'],
                                                'm_checkio',
                                                response['title'],
                                                response['description'].replace('\n', ' ')[:50],
                                                tagnames=tagnames)
        memopla_command.flush()
        memopla_command.commit()
        checkio_command.commit()
        return redirect(url_for('index'))
