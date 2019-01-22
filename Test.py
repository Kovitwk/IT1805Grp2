from flask import Flask, flash, redirect, url_for, session, render_template, Session
from flask_babel import *
import shelve
from Record import Record
from Convert import Convert
from Converter import *
from AddRecordForm import *

app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)
app.secret_key = 'Do not tell anyone'


@babel.localeselector
def get_locale():
    return 'en'


@app.route("/")
def main():
    return render_template("sportshome.html")


@app.route("/sportshome")
def home():
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
            db = shelve.open('storage', 'c')

            try:
                recordList = db['Records']

            except:
                print("failed to open database")

            new_record = Record(form.height.data, form.weight.data, form.id.data)
            recordList[form.id.data] = new_record
            db['Records'] = recordList
            print(db['Records'])
            db.close()

            return redirect(url_for('summary'))

    return render_template('record.html', form=form)


@app.route('/summary')
def summary():
    dictionary = {}
    db = shelve.open('storage', 'c')
    dictionary = db['Records']
    db.close()

    list = []
    for key in dictionary:
        item = dictionary.get(key)
        list.append(item)

    return render_template('summary.html', records=list, count=len(list))


if __name__ == "__main__":
    app.run(debug=True)
