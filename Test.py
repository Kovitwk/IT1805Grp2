from flask import *
from flask_babel import *
import shelve
from Record import Record
from AddRecordForm import *

app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)


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
    print('The method is ' + request.method)
    if request.method == 'POST':
        if form.validate() == 0:
            print('All fields are required.')

        else:
            recordList = {}
            db = shelve.open('storage.db', 'c')

            try:
                recordList = db['Records']

            except:
                print("failed to open database")
            new_record = Record(form.height.data, form.weight.data)
            recordList[new_record.get_height()] = new_record
            db['Records'] = recordList
            db.close()

            return redirect(url_for('summary.html'))

    return render_template('record.html', form=form)


@app.route('/summary')
def summary():
    dictionary = {}
    db = shelve.open('storage.db', 'r')
    dictionary = db['Records']
    db.close()

    # convert dictionary to list
    list = []
    for key in dictionary:
        item = dictionary.get(key)
        # print("here: ", user.get_userID())
        # print("here:", user.get_firstname())
        list.append(item)
    return render_template('summary.html', records=list, count=len(list))


if __name__ == "__main__":
    app.run(debug=True)
