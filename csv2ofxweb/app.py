import os

from flask import Flask, render_template, make_response
from flask.ext import wtf, bootstrap
from flask.ext.wtf import file as wtfile
import wtforms

from csv2ofx import fokus

app = Flask(__name__)
bootstrap.Bootstrap(app)


class Form(wtf.Form):
    bank = wtforms.SelectField('Bank', choices=[('fokus', 'Fokus')])
    account = wtforms.TextField('Account number')
    csv = wtfile.FileField('CSV')


@app.route('/', methods=('GET', 'POST'))
def page():
    form = Form()
    if form.validate_on_submit():
        response = make_response(
            ofxify(form.bank.data, form.account.data, form.csv.data))
        response.headers['Content-Type'] = 'application/x-ofx'
        attachment_name = os.path.splitext(form.csv.data.filename)[0]
        response.headers['Content-Disposition'] = (
            'attachment; filename={}.ofx'.format(attachment_name))
        return response
    else:
        return render_template('form.html', form=form)


def ofxify(bank, account, csv):
    if bank == 'fokus':
        return fokus.FokusBankCSV2OFX(
            'Fokus bank', account, 'NOK').build_ofx(csv)


def main():
    app.config.from_pyfile('app.cfg')
    app.run(debug=True)
