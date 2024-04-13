

from flask import Flask, render_template, send_from_directory, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.fields.simple import TextAreaField
from wtforms.validators import Email, DataRequired
import smtplib
import os
'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

# SENDING MAIL FROM CONTACT PAGE
OWN_EMAIL = os.environ.get('OWN_EMAIL')
OWN_PASSWORD = os.environ.get('OWN_PASSWORD')


def send_email(form):
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(user=OWN_EMAIL, password=OWN_PASSWORD)
        message = (f"Subject:Message from My Portfolio site \n\nName: {form.full_name.data}\nEmail: {form.email.data}"
                   f"\nPhone: {form.phone_number.data}\nMessage:{form.message.data}")
        connection.sendmail(from_addr=OWN_EMAIL, to_addrs=OWN_EMAIL,
                            msg=message)


# Create Flask WTF Contact form
class ContactForm(FlaskForm):
    full_name = StringField(
        label='Full name',
        validators=[DataRequired()],
        render_kw={
            "placeholder": "Enter your name",
        }
    )
    email = StringField(
        label='Email address', validators=[Email()],
        render_kw={
            "placeholder": "Enter your email address",
        }
    )
    phone_number = StringField(
        label='Phone number',
        validators=[DataRequired(), validators.Length(min=10),
                    validators.Regexp(regex=r'^\+?\d{8,15}$', message="Invalid phone number")],
        render_kw={
            "placeholder": "Enter your phone number"
        }
    )
    message = TextAreaField(
        'Message',
        render_kw={
            "rows": 4, "cols": 10,
            "placeholder": "Enter your message"
        },
        validators=[DataRequired()],
    )
    send = SubmitField(label="Send",
                       render_kw={
                           'class': 'btn btn-primary btn-lg d-block mx-auto ',
                           'style': 'width: 50%;'
                       })


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_KEY')
bootstrap = Bootstrap5(app)  # initialise bootstrap-flask


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/resume')
def resume():
    return render_template('resume.html')


@app.route('/projects')
def project():
    return render_template('projects.html')


@app.route('/contact', methods=["GET", "POST"])
def contact():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        flash('📨 Message sent successfully!', 'success')
        send_email(form=contact_form)
        return redirect(url_for('contact', form=contact_form))

    return render_template('contact.html', form=contact_form)


@app.route("/download")
def download_resume():
    return send_from_directory('static', path="file/RESUME_SDE_KARTHICK.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=False)
