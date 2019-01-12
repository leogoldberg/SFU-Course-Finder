from flask import Flask, request, render_template, flash, redirect, url_for, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, SelectField, validators
from config import config

app = Flask(__name__)


# Config MySQL
app.config['MYSQL_HOST'] = config.host
app.config['MYSQL_USER'] = config.user
app.config['MYSQL_PASSWORD'] = config.password
app.config['MYSQL_DB'] = config.db
app.config['MYSQL_CURSORCLASS'] = config.cursorclass

# init MySql
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/schedules', methods=['GET', 'POST'])
def schedules():

    form = ScheduleForm(request.form)
    if request.method == 'POST' and form.validate():
        room = form.room.data
        time = form.time.data
        day = form.day.data
        print(room)
        print(time)
        print(day)
        # create cursor
        conn = mysql.connection.cursor()

        result = conn.execute(
            "SELECT * FROM schedules WHERE room = %s AND start_time<= %s AND end_time>= %s AND day = %s", [room, time, time, day])

        courses = conn.fetchone()
        print(result)
        print(courses)
        # close Connection
        conn.close()

        if result > 0:
            return render_template('schedules.html', form=form, courses=courses)
        else:
            msg = 'No such classes exist'
            return render_template('schedules.html', form=form, courses="no class at this time!")

    return render_template('schedules.html', form=form, courses="no class at this time!")

# Schedule Form Class


class ScheduleForm(Form):
    room = StringField('Room', [validators.Length(min=4, max=30)])
    time = StringField('Time', [validators.Length(min=2, max=10)])
    day = SelectField('Day', choices=[('Mo', 'Monday'), ('Tu', 'Tuesday'),
                                      ('We', 'Wednesday'), ('Th', 'Thursday'), ('Fr', 'Friday')])


if __name__ == '__main__':
    app.run(debug=True)
