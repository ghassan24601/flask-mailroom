import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY').encode()


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            donor = Donor.get(Donor.name == request.form['name'])
        except Donor.DoesNotExist:
            donor = Donor(name=request.form['name'])
            donor.save()
        donation = Donation(donor_id=donor.id, value=request.form['donation'])
        donation.save()
        return redirect(url_for('all'))
    else:
        return render_template('create.jinja2')


if __name__ == "__main__":
    app.run()

