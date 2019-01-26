from flask import Flask, render_template, request, redirect, url_for, flash
from flask_babel import *
from simData import *
from Record import Record
from AddRecordForm import *
from dietRecipe import *
import shelve
import AdaptedSimulationCode as simCode


app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)


@babel.localeselector
def get_locale():
    return 'ms'


@app.route("/")
def main():
    return render_template("SmartLivingHomepage.html")


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

    # convert dictionary to list
    list = []
    for key in dictionary:
        item = dictionary.get(key)
        list.append(item)
    return render_template('summary.html', records=list, count=len(list))

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

@app.route('/<string:id>/delete', methods=('GET', 'POST'))
def delete(id):
    delete_recipe(id)
    posts = get_recipes()
    return render_template('index.html', posts=posts)


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

@app.route('/Sim.html', methods=['GET', 'POST'])
def sim():
    calc = simData(request.form)
    if request.method == 'POST':
            if calc.validate():
                with shelve.open('simStorage') as simStorage:
                    simStorage['ledNum'] = int(calc.led.data)
                    simStorage['cflNum'] = int(calc.cfl.data)
                    simStorage['incNum'] = int(calc.inc.data)
                    simStorage['toiletNum'] = int(calc.toish.data)
                    simStorage['toiletType'] = calc.toitype.data
                    led = simStorage['ledNum']
                    cfl = simStorage['cflNum']
                    inc = simStorage['incNum']
                    toitype = simStorage['toiletType']
                finalWatt = simCode.calcWatt()
                finalPrice = simCode.calcWattPrice()
                dailyWatt = round(finalWatt / 30, 2)
                dailyPrice = round(finalPrice / 30, 2)
                yearlyWatt = round(finalWatt * 12, 2)
                yearlyPrice = round(finalPrice * 12, 2)
                cubmtrperday = simCode.calcCubmtr()
                cubmtrPrice = simCode.calcCubmtrPrice()
                dailyCubmtr = round(cubmtrperday / 30, 2)
                dailyCubmtrPrice = round(cubmtrPrice / 30, 2)
                yearlyCubmtr = round(cubmtrperday * 12, 2)
                yearlyCubmtrPrice = round(cubmtrPrice * 12, 2)
                tipElc = simCode.tipsElc()
                tipWtr = simCode.tipsWtr()
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
                return render_template("Sim.html", toitype=toitype, inc=inc, cfl=cfl, led=led, replaceOldorConv=replaceOldorConv, saveSmartW=saveSmartW, saveSmartE=saveSmartE, replaceCfl=replaceCfl, replaceInc=replaceInc, openTab=openTab, cubmtrPrice=cubmtrPrice, cubmtrperday=cubmtrperday,
                                       yearlyCubmtrPrice=yearlyCubmtrPrice, yearlyCubmtr=yearlyCubmtr,
                                       dailyCubmtrPrice=dailyCubmtrPrice, dailyCubmtr=dailyCubmtr,
                                       yearlyPrice=yearlyPrice, yearlyWatt=yearlyWatt, dailyPrice=dailyPrice,
                                       dailyWatt=dailyWatt, finalPrice=finalPrice, finalWatt=finalWatt,
                                       calc=calc)
            else:
                error = 'Only numbers lower than 100 are allowed.'
                return render_template("Sim.html", error=error, calc=calc)
    else:
        return render_template("Sim.html", calc=calc)

if __name__ == "__main__":
    app.run(debug=True)
