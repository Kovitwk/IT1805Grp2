from flask import *
from simData import *

import shelve
from Record import Record
from AddRecordForm import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'iufnaofiLKE'


@app.route("/")
def main():
    return render_template("SmartLivingHomepage.html")


@app.route("/sportshome.html")
def home():
    return render_template("sportshome.html")


@app.route("/sportsavatar.html")
def avatar():
    return render_template("")


@app.route("/sportsworkout.html")
def workout():
    return render_template("sportsworkout.html")


@app.route('/record.html', methods=['GET', 'POST'])
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

    return render_template('/record.html', form=form)


@app.route('/summary.html')
def summary():
    dictionary = {}
    db = shelve.open('storage.db', 'r')
    dictionary = db['Records']
    db.close()

    # convert dictionry to list
    list = []
    for key in dictionary:
        item = dictionary.get(key)
        # print("here: ", user.get_userID())
        # print("here:", user.get_firstname())
        list.append(item)
    return render_template('summary.html', records=list, count=len(list))


@app.route('/Sim.html', methods=['GET', 'POST'])
def sim():
    calc = simData()
    if request.method == 'GET':
        return render_template("Sim.html", calc=calc)
    elif request.method == 'POST':
        return render_template("SimResults.html", calc=calc)


if __name__ == "__main__":
    app.run(debug=True)
