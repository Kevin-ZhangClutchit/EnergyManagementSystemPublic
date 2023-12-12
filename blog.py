from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, make_response
)
from flask_login import current_user
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from datetime import date, timedelta, datetime
from matplotlib.figure import Figure
from io import BytesIO
import base64

bp = Blueprint('blog', __name__)


def plot_past7day_daily(last7day):
    # https://matplotlib.org/stable/gallery/user_interfaces/web_application_server_sgskip.html
    # current_date = date.today()
    current_date = date.fromisoformat('2023-12-11')  # demo purpose should be date.today()
    date_dict = {}
    for single_date in (current_date - timedelta(n) for n in range(7)):
        date_dict.update({single_date: 0})
    for single_day_sum in last7day:
        # assert single_day_sum['date'] in date_dict.keys()
        date_dict.update({single_day_sum['date']: single_day_sum['energysum']})
    dates = list(date_dict.keys())
    values = list(date_dict.values())
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    bars = ax.bar(dates, values, width=0.8, align='center')
    for bar in bars:
        y_val = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, y_val, round(y_val, 2), ha='center', va='bottom')
    ax.set_xlabel('Date')
    ax.set_ylabel('Daily Energy Consumption')
    ax.set_title('Daily Energy Consumption in past 7 days')
    fig.autofmt_xdate()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    img = base64.b64encode(buf.getbuffer()).decode("ascii")
    return img


@bp.route('/')
@login_required
def index():
    response = make_response(render_template('blog/index.html'))
    response.headers['Content-Security-Policy'] = "default-src 'self';"
    return response


@bp.route('/view1/')
@login_required
def energy_view_last7day():
    userID = current_user.id
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'SELECT date(timestamp) as date, sum(value) as energysum'
        ' FROM user NATURAL JOIN customer_service NATURAL JOIN device NATURAL JOIN datas'
        ' where user.cid = %s and eventLabel = "energy use"'
        ' AND timestamp >= DATE_SUB(%s, INTERVAL 7 DAY)'
        ' AND date(timestamp) <= %s group by date(timestamp)',
        (userID, '2023-12-11', '2023-12-11')
    )
    # For demo purpose, here we set to 2023-12-11, it should be CurDate()
    columns = [column[0] for column in cursor.description]
    last7day = [dict(zip(columns, row)) for row in cursor.fetchall()]
    # print(last7day)
    last7day_img = plot_past7day_daily(last7day)
    return render_template('blog/last7day.html', last7day_img=last7day_img)


def plot_device_monthly(data, year, month):
    img = None
    # https://matplotlib.org/stable/gallery/user_interfaces/web_application_server_sgskip.html
    x = []
    y = []
    for data_frame in data:
        x.append(data_frame['type'])
        y.append(data_frame['avgEnergyCost'])

    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.pie(y, labels=x, autopct='%1.1f%%', startangle=120)
    ax.axis('equal')
    ax.set_title(f'Monthly Energy Cost Distribution in {year}-{month}')
    buf = BytesIO()
    fig.savefig(buf, format="png")
    img = base64.b64encode(buf.getbuffer()).decode("ascii")
    return img


@bp.route('/view2/', methods=['GET', 'POST'])
@login_required
def energy_view_devicelastmonth():
    selected_year = None
    selected_month = None
    plot_image = None
    if request.method == 'POST':
        selected_year = request.form.get('year')
        selected_month = request.form.get('month')
        userID = current_user.id
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'SELECT type, round(sum(value)/count(distinct deviceid),2) as avgEnergyCost '
            'from datas natural join device natural join servicelocation natural join customer_service '
            'natural join user'
            ' where user.cid = %s and  month(timestamp)= %s and year(timestamp)= %s '
            'and eventLabel = "energy use" group by type',
            (userID, selected_month, selected_year)
        )
        columns = [column[0] for column in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        if len(data) > 0:
            plot_image = plot_device_monthly(data, selected_year, selected_month)
    return render_template('blog/devicelastmonth.html', selected_year=selected_year, selected_month=selected_month,
                           plot_image=plot_image)


def plot_location_monthly(data, year, month):
    img = None
    x = []
    y = []
    for data_frame in data:
        x.append(data_frame['addr'] + " " + data_frame["unitNumber"])
        y.append(data_frame['avgEnergyCost'])

    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.pie(y, labels=x, autopct='%1.1f%%', startangle=120)
    ax.axis('equal')
    ax.set_title(f'Monthly Energy Cost Distribution according to Location in {year}-{month}')
    buf = BytesIO()
    fig.savefig(buf, format="png")
    img = base64.b64encode(buf.getbuffer()).decode("ascii")
    return img


@bp.route('/view3/', methods=['GET', 'POST'])
@login_required
def energy_view_locationlastmonth():
    selected_year = None
    selected_month = None
    plot_image = None
    if request.method == 'POST':
        selected_year = request.form.get('year')
        selected_month = request.form.get('month')
        userID = current_user.id
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'SELECT sLid, addr, unitNumber, round(sum(value)/count(distinct sLid),2) as avgEnergyCost '
            'from datas natural join device natural join servicelocation '
            'natural join customer_service natural join user'
            ' where user.cid = %s and  month(timestamp)= %s and year(timestamp)= %s '
            'and eventLabel = "energy use" group by sLid',
            (userID, selected_month, selected_year)
        )
        columns = [column[0] for column in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        if len(data) > 0:
            plot_image = plot_location_monthly(data, selected_year, selected_month)
    return render_template('blog/locationlastmonth.html', selected_year=selected_year, selected_month=selected_month,
                           plot_image=plot_image)


def plot_similar_data(oridata, similardata, year, month):
    img = None
    y = []
    y.append(oridata[0]['totalCost'])
    y.append(similardata[0]['avgCost'])
    label = ["Selected Location", "Similar Average"]
    # print(y)

    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    bars = ax.bar(label, y)
    for bar in bars:
        y_val = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, y_val, round(y_val, 2), ha='center', va='bottom')
    ax.set_ylabel('Energy Consumption')
    ax.set_title('Average Energy Consumption in ' + year + "-" + month)
    ax.legend()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    img = base64.b64encode(buf.getbuffer()).decode("ascii")
    return img


@bp.route('/view4/', methods=['GET', 'POST'])
@login_required
def energy_view_similarProperty():
    selected_year = None
    selected_month = None
    plot_image = None
    addr = None
    unitNumber = None
    inputs = None

    userID = current_user.id
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'SELECT sLid,addr, unitNumber,squareFootage from'
        ' user natural join customer_service natural join servicelocation'
        ' where user.cid = %s',
        (userID,)
    )
    columns = [column[0] for column in cursor.description]
    inputs = [dict(zip(columns, row)) for row in cursor.fetchall()]
    if len(inputs) == 0:
        inputs = None
    if request.method == 'POST':
        addr, unitNumber, sLid, squareFootage = request.form.get('location').split(',')
        selected_year = request.form.get('year')
        selected_month = request.form.get('month')
        userID = current_user.id
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'SELECT ifnull(sum(value)/count(distinct sLid),0) as avgCost '
            'from user natural join customer_service natural join servicelocation natural join device'
            ' natural join datas'
            ' where user.cid <> %s and  month(timestamp)= %s and year(timestamp)= %s '
            'and eventLabel = "energy use" and squareFootage >= %s*0.9 and squareFootage <= %s*1.1',
            (userID, selected_month, selected_year, squareFootage, squareFootage)
        )
        columns = [column[0] for column in cursor.description]
        avg_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        # print(avg_data)
        cursor.execute(
            'SELECT ifnull(sum(value),0) as totalCost '
            'from user natural join customer_service natural join servicelocation natural join device'
            ' natural join datas'
            ' where user.cid = %s and  month(timestamp)= %s and year(timestamp)= %s '
            'and eventLabel = "energy use" and sLid = %s',
            (userID, selected_month, selected_year, sLid)
        )
        columns = [column[0] for column in cursor.description]
        total_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        # print(total_data)
        if len(avg_data) > 0:
            pass
            plot_image = plot_similar_data(oridata=total_data, similardata=avg_data,
                                           year=selected_year, month=selected_month)
    return render_template('blog/similarProperty.html', selected_year=selected_year,
                           selected_month=selected_month, inputs=inputs, img=plot_image,
                           addr=addr, unitNumber=unitNumber)


def plot_price(data, year, month):
    img = None
    x = []
    y = []
    for data_frame in data:
        x.append(str(data_frame['fromtime']) + "-" + str(data_frame["endtime"]))
        y.append(data_frame['bill'])

    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.pie(y, labels=x, autopct='%1.1f%%', startangle=120)
    ax.axis('equal')
    ax.set_title(f'Energy Price Consumption According to Time Period in {year}-{month}')
    buf = BytesIO()
    fig.savefig(buf, format="png")
    img = base64.b64encode(buf.getbuffer()).decode("ascii")
    return img


@bp.route('/view5/', methods=['GET', 'POST'])
@login_required
def energy_view_price():
    selected_year = None
    selected_month = None
    plot_image = None
    if request.method == 'POST':
        selected_year = request.form.get('year')
        selected_month = request.form.get('month')
        userID = current_user.id
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'SELECT fromtime,endtime, sum(price*value) as bill  '
            'FROM datas natural join device natural join servicelocation '
            'natural join customer_service natural join user'
            ' left outer join price on time(datas.timestamp) >= fromtime and time(datas.timestamp) <= endtime and'
            ' servicelocation.zipcode=price.zipcode'
            ' where user.cid = %s and  month(timestamp)= %s and year(timestamp)= %s '
            'and eventLabel = "energy use" group by fromtime,endtime',
            (userID, selected_month, selected_year)
        )
        columns = [column[0] for column in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        if len(data) > 0:
            plot_image = plot_price(data, selected_year, selected_month)
    return render_template('blog/price.html', selected_year=selected_year, selected_month=selected_month,
                           plot_image=plot_image)


@bp.route('/<int:id>/profile', methods=['GET', 'POST'])
@login_required
def editProfile(id):
    if id != current_user.id:
        abort(403)
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT first_name, last_name, billAddr '
                   'FROM user where user.cid = %s',
                   (id,))
    columns = [column[0] for column in cursor.description]
    res = cursor.fetchone()
    user_info = dict(zip(columns, res))
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        billAddr = request.form['billAddr']
        error = None

        if not first_name or not last_name or not billAddr:
            error = 'A required field is empty.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'UPDATE user SET first_name = %s, last_name = %s, billAddr = %s'
                ' WHERE cid = %s',
                (first_name, last_name, billAddr, current_user.id)
            )
            db.commit()
            return redirect(url_for('index', id=current_user.id))
    return render_template('blog/editProfile.html', user_info=user_info)
