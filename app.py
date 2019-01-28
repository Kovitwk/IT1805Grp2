from flask import *
from persistence import *
from flask_babel import *
from Record import Record
from Convert import Convert
from Converter import *
from AddRecordForm import *
from simData import *
from dietRecipe import *
import shelve
import functools
import AdaptedSimulationCode as simCode
import time

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='dev')
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
        return render_template('SmartLivingHomepage.html', user=session['user_name'])
    else:
        return render_template('login.html')


@app.route('/diet')
def diet():
    posts = get_recipes()
    return render_template('diet.html', posts=posts)


@app.route('/dietUpdate', methods=('GET', 'POST'))
def update():
    recipeBlock = createRecipe(request.form)
    if request.method == 'POST':
        if request.form['form_submit'] == 'delete':
            delete_recipe()
            return redirect(url_for('diet'))
    else:
        delete = True
        return render_template('dietUpdate.html', recipeBlock=recipeBlock, delete=delete)


@app.route('/dietCreate', methods=('GET', 'POST'))
def create():
    recipeBlock = createRecipe(request.form)
    if request.method == "POST":
        if recipeBlock.validate():
            create_recipe(recipeBlock.title.data, recipeBlock.body.data, recipeBlock.image.data)
            return redirect(url_for('diet'))
        else:
            print('Not valid')
            return redirect(url_for('diet'))
    else:
        return render_template('dietCreate.html', recipeBlock=recipeBlock)


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
        if username == 'Admin' and password == 'Admin123':
            return redirect(url_for('index'))
        else:
            user = get_user(username, password)
            if user is None:
                error = 'Wrong username and password'
            else:
                session['id'] = user.get_id()
                session['user_name'] = user.get_username()
                return redirect(url_for('index'))
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

'''
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
'''

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
    dictionary = {}
    db = shelve.open('fitness', 'c')
    dictionary = db['Records']
    print('This is dict', dictionary)
    db.close()

    level = ""
    lines = []
    text = {}
    k = 1

    for i in dictionary:
        print('This is i', i)
        if i == session['user_name']:
            item = dictionary.get(i)
            print("This is item", item)
            print("item bmi", item.get_bmi())
            level = item.get_bmi()
            print("This is level", level)

            if level < 18:
                file = open('under.txt', 'r')
                content = file.readline()
                while content != "":
                    content = file.readline()
                    lines.append(content)
                    print(content)
                file.close()
                for l in range(len(lines)):
                    text[k] = lines[l]
                    l += 2
                    k += 1
                print(text)

            if 18 <= level <= 25:
                file = open('normal.txt', 'r')
                content = file.readline()
                while content != "":
                    content = file.readline()
                    lines.append(content)
                    print(content)
                file.close()
                for l in range(len(lines)):
                    text[k] = lines[l]
                    l += 2
                    k += 1
                print(text)

            if level > 25:
                file = open('over.txt', 'r')
                content = file.readline()
                while content != "":
                    content = file.readline()
                    lines.append(content)
                    print(content)
                file.close()
                for l in range(len(lines)):
                    text[k] = lines[l]
                    l += 2
                    k += 1
                print(text)

    return render_template("sportsworkout.html", fitness=level, workout1=text[1], workout2=text[2], workout3=text[3])


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

            try:
                height = float(form.height.data)
                weight = float(form.weight.data)
                new_record = Record(height, weight, time.strftime("%d/%m/%Y"))
                recordList[session['user_name']] = new_record
                db['Records'] = recordList
                print(db['Records'])
                db.close()

            except ValueError:
                print('Failed to submit form')
                return redirect(url_for('record'))

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
            print("This is item", item)
            list.append(item)

    return render_template('summary.html', records=list, count=len(list), user=session['user_name'])


@app.route('/Sim.html', methods=['GET', 'POST'])
def sim():
    print(session['user_name'])
    calc = simData(request.form)
    if request.method == 'POST':
            if calc.validate():
                simCode.storeData(calc.led.data, calc.cfl.data, calc.inc.data,
                                  calc.toish.data, calc.toitype.data,
                                  session['user_name'])
                with shelve.open('simStorage') as simStorage:
                        led = simStorage[session['user_name']].led
                        cfl = simStorage[session['user_name']].cfl
                        inc = simStorage[session['user_name']].inc
                        toitype = simStorage[session['user_name']].toitype
                        finalWatt = simCode.calcWatt(session['user_name'])
                        finalPrice = simCode.calcWattPrice(session['user_name'])
                        dailyWatt = round(finalWatt / 30, 2)
                        dailyPrice = round(finalPrice / 30, 2)
                        yearlyWatt = round(finalWatt * 2, 2)
                        yearlyPrice = round(finalPrice * 12, 2)
                        cubmtrperday = simCode.calcCubmtr(session['user_name'])
                        cubmtrPrice = simCode.calcCubmtrPrice(session['user_name'])
                        dailyCubmtr = round(cubmtrperday / 30, 2)
                        dailyCubmtrPrice = round(cubmtrPrice / 30, 2)
                        yearlyCubmtr = round(cubmtrperday * 12, 2)
                        yearlyCubmtrPrice = round(cubmtrPrice * 12, 2)
                        tipElc = simCode.tipsElc(session['user_name'])
                        tipWtr = simCode.tipsWtr(session['user_name'])
                        global replaceInc
                        global replaceCfl
                        global saveSmartE
                        global saveSmartW
                        global replaceOldorConv
                        replaceInc = False
                        replaceCfl = False
                        saveSmartE = False
                        saveSmartW = False
                        replaceOldorConv = False
                        for i in tipElc:
                            if i == 'replaceInc':
                                replaceInc = True
                            if i == 'replaceCfl':
                                replaceCfl = True
                            if i == 'saveSmartE':
                                saveSmartE = True
                        for i in tipWtr:
                            if i == 'replaceOldorConv':
                                replaceOldorConv = True
                            if i == 'saveSmartW':
                                saveSmartW = True
                        openTab = True
                        return render_template("Sim.html", toitype=toitype, inc=inc, cfl=cfl, led=led,
                                               replaceOldorConv=replaceOldorConv, saveSmartW=saveSmartW,
                                               saveSmartE=saveSmartE, replaceCfl=replaceCfl, replaceInc=replaceInc,
                                               openTab=openTab, cubmtrPrice=cubmtrPrice, cubmtrperday=cubmtrperday,
                                               yearlyCubmtrPrice=yearlyCubmtrPrice, yearlyCubmtr=yearlyCubmtr,
                                               dailyCubmtrPrice=dailyCubmtrPrice, dailyCubmtr=dailyCubmtr,
                                               yearlyPrice=yearlyPrice, yearlyWatt=yearlyWatt, dailyPrice=dailyPrice,
                                               dailyWatt=dailyWatt, finalPrice=finalPrice, finalWatt=finalWatt,
                                               calc=calc)
            else:
                error = 'Only numbers lower than 100 are allowed.'
                return render_template("Sim.html", error=error, calc=calc)
    else:
        with shelve.open('simStorage') as simStorage:
            if session['user_name'] in simStorage:
                return redirect(url_for("simDisplay"))
            else:
                return render_template("Sim.html", calc=calc)


@app.route('/SimDisplay.html', methods=['GET', 'POST'])
def simDisplay():
    if request.method == "POST":
        with shelve.open('simStorage') as simStorage:
            del simStorage[session['user_name']]
            return redirect(url_for('sim'))
    else:
        with shelve.open('simStorage') as simStorage:
            led = simStorage[session['user_name']].led
            cfl = simStorage[session['user_name']].cfl
            inc = simStorage[session['user_name']].inc
            toi = simStorage[session['user_name']].toish
            toitype = simStorage[session['user_name']].toitype
            finalWatt = simCode.calcWatt(session['user_name'])
            finalPrice = simCode.calcWattPrice(session['user_name'])
            dailyWatt = round(finalWatt / 30, 2)
            dailyPrice = round(finalPrice / 30, 2)
            yearlyWatt = round(finalWatt * 12, 2)
            yearlyPrice = round(finalPrice * 12, 2)
            cubmtrperday = simCode.calcCubmtr(session['user_name'])
            cubmtrPrice = simCode.calcCubmtrPrice(session['user_name'])
            dailyCubmtr = round(cubmtrperday / 30, 2)
            dailyCubmtrPrice = round(cubmtrPrice / 30, 2)
            yearlyCubmtr = round(cubmtrperday * 12, 2)
            yearlyCubmtrPrice = round(cubmtrPrice * 12, 2)
            tipElc = simCode.tipsElc(session['user_name'])
            tipWtr = simCode.tipsWtr(session['user_name'])
            global replaceInc
            global replaceCfl
            global saveSmartE
            global saveSmartW
            global replaceOldorConv
            replaceInc = False
            replaceCfl = False
            saveSmartE = False
            saveSmartW = False
            replaceOldorConv = False
            for i in tipElc:
                if i == 'replaceInc':
                    replaceInc = True
                if i == 'replaceCfl':
                    replaceCfl = True
                if i == 'saveSmartE':
                    saveSmartE = True
            for i in tipWtr:
                if i == 'replaceOldorConv':
                    replaceOldorConv = True
                if i == 'saveSmartW':
                    saveSmartW = True
            openTab = True
            return render_template("SimDisplay.html",toi=toi, toitype=toitype, inc=inc, cfl=cfl, led=led,
                                   replaceOldorConv=replaceOldorConv, saveSmartW=saveSmartW, saveSmartE=saveSmartE,
                                   replaceCfl=replaceCfl, replaceInc=replaceInc, openTab=openTab,
                                   cubmtrPrice=cubmtrPrice, cubmtrperday=cubmtrperday,
                                   yearlyCubmtrPrice=yearlyCubmtrPrice, yearlyCubmtr=yearlyCubmtr,
                                   dailyCubmtrPrice=dailyCubmtrPrice, dailyCubmtr=dailyCubmtr,
                                   yearlyPrice=yearlyPrice, yearlyWatt=yearlyWatt, dailyPrice=dailyPrice,
                                   dailyWatt=dailyWatt, finalPrice=finalPrice, finalWatt=finalWatt)



if __name__ == '__main__':
    app.run(debug = True)
