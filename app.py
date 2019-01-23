from flask import *
from persistence import *
import functools
from flask_babel import *
import shelve
from Record import Record
from Convert import Convert
from Converter import *
from AddRecordForm import *

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev'
)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)
app.secret_key = 'Test123456543$2313fd$@#@%^21dz'


@babel.localeselector
def locale_selector():
    return 'en'


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session['id'] is None:
            return redirect(url_for('login'))
        return view(**kwargs)

    return wrapped_view


@app.route('/test')
def test():
    return render_template('test222.html')


@app.route('/init')
def init():
    init_db()
    return 'db initialised'


@app.route('/')
def index():
    if 'id' in session:
        posts = get_blogs()
        return render_template('index.html', user=session['user_name'])
    else:
        return render_template('login.html')


@app.route('/login',  methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            user = get_user(username, password)
            if user is None:
                error = 'Wrong username and password'
            else:
                session['id'] = user.get_id()
                session['user_name'] = user.get_username()
                return redirect(url_for('homepage'), user=session['user_name'])
        flash(error)
    return render_template('login.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            create_user(username, password, email)
            return redirect(url_for('login'))
        flash(error)
    return render_template('register.html')


@app.route('/<string:id>/update', methods=('GET', 'POST'))
def update(id):
    post = get_blog(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            update_blog(post)
            return redirect(url_for('homepage'))

    return render_template('update.html', post=post)


@app.route('/<string:id>/delete', methods=('GET', 'POST'))
def delete(id):
    delete_blog(id)
    posts = get_blogs()
    return render_template('index.html', user=session['user_name'])


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            create_blog(session['user_name'], title, body)
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/homepage.html')
def homepage():
    return render_template('test222.html', user=session['user_name'])


@app.route('/ProfilePage.html')
def ProfilePage():
    return render_template('ProfilePage.html')


@app.route("/sportshome", methods=['POST', 'GET'])
def home():
    '''
    if request.method == 'POST':
        if request.form['btn'] == 'en':
            @babel.localeselector
            def get_locale():
                return render_template("sportshome.html"), 'en'

        if request.form['btn'] == 'ms':
            @babel.localeselector
            def get_locale():
                return render_template("sportshome.html"), 'ms'
    '''

    return render_template("sportshome.html")


@app.route("/sportsavatar")
def avatar():
    return render_template("sportsavatar.html")


@app.route("/sportsworkout")
def workout():
    return render_template("sportsworkout.html")


@app.route('/record', methods=['GET', 'POST'])
def record():
    form = AddRecordForm(request.form)
    form1 = Converter(request.form)
    print('The method is ' + request.method)

    if request.method == 'POST':
        if form.validate() == 0:
            print('All fields are required.')

        if request.form["btn"] == "Convert":
            convert = Convert(form1.heightconvert.data, form1.weightconvert.data)
            flash('%d cm is %.2f m' % (form1.heightconvert.data, convert.get_heightc()))
            flash('%d lbs is %.2f kg' % (form1.weightconvert.data, convert.get_weightc()))

        elif request.form["btn"] == "Submit":
            recordList = {}
            db = shelve.open('fitness', 'c')

            try:
                recordList = db['Records']

            except:
                print("failed to open database")

            new_record = Record(form.height.data, form.weight.data)
            recordList[session['user_name']] = new_record
            db['Records'] = recordList
            print(db['Records'])
            db.close()

            return redirect(url_for('summary'))

    return render_template('record.html', form=form)


@app.route('/summary')
def summary():
    dictionary = {}
    db = shelve.open('fitness', 'c')
    dictionary = db['Records']
    print('This is dict', dictionary)
    db.close()

    list = []
    for i in dictionary:
        print('This is i', i)
        if i == session['user_name']:
            item = dictionary.get(i)
            list.append(item)

    return render_template('summary.html', records=list, count=len(list), user=session['user_name'])


if __name__ == '__main__':
    app.run(debug = True)
