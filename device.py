from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.auth import login_required
from flaskr.db import get_db
from werkzeug.exceptions import abort
from flask_login import current_user
from matplotlib.figure import Figure
from io import BytesIO
import base64
bp = Blueprint('device', __name__, url_prefix='/device')

def isValidAccess(id, sLid):
    if current_user.id != id:
        return False
    else:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT cid from customer_service WHERE sLid = %s'
                       , (sLid,))
        columns = [column[0] for column in cursor.description]
        res = cursor.fetchone()
        if res is None:
            return False
        cid = dict(zip(columns, res))

    return current_user.id == cid['cid']
@bp.route('/<int:id>/<int:sLid>/location_main')
@login_required
def locationMain(id, sLid):
    if not isValidAccess(id,sLid):
        abort(403)
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM device NATURAL JOIN model WHERE sLid = %s'
                   , (sLid,))

    columns = [column[0] for column in cursor.description]
    devices = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return render_template('device/locationMain.html', devices=devices, num=len(devices), sLid=sLid
                           )


@bp.route('/<int:id>/<int:sLid>/addDevice', methods=('GET', 'POST'))
@login_required
def addDevice(id, sLid):

    if request.method == 'GET':
        # https://stackoverflow.com/questions/6954556/show-a-second-dropdown-based-on-previous-dropdown-selection
        db = get_db()
        cursor = db.cursor()
        type_list = ["Light", "Refrigerator", "Air-Conditioner"]
        type_dict = {}
        for type in type_list:
            cursor.execute('SELECT * from model where modeltype = %s'
                           , (type,))
            columns = [column[0] for column in cursor.description]
            models = [dict(zip(columns, row)) for row in cursor.fetchall()]
            type_dict.update({type: models})
    elif request.method == 'POST':
        type = request.form.get('types')
        if not type:
            abort(403)
        modelid = request.form.get(type)
        error = None

        if not type or not modelid:
            error = 'A required field is empty.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO device (type, modelid, SLid)'
                ' VALUES (%s, %s, %s)',
                (type, modelid, sLid)
            )
            db.commit()
            return redirect(url_for('device.locationMain', id=id, sLid=sLid))

    return render_template('device/addDevice.html', type_dict=type_dict, type_list=type_list,sLid=sLid)

def isValidAccessDevice(id, sLid,deviceid):
    if not isValidAccess(id,sLid):
        return False
    else:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT cid,sLid from customer_service natural join device WHERE deviceid = %s'
                       , (deviceid,))
        columns = [column[0] for column in cursor.description]
        res = cursor.fetchone()
        if res is None:
            return False
        res_dict = dict(zip(columns, res))

    return current_user.id == res_dict['cid'] and sLid == res_dict['sLid']

def plot_year_image(year_data):
    sorted_data = sorted(year_data, key=lambda x: (x['year'], x['month']))
    x_values = [f"{entry['year']}-{entry['month']:02d}" for entry in sorted_data]
    y_values = [entry['total_energy'] for entry in sorted_data]
    fig = Figure(figsize=(8, 6))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(x_values, y_values)
    for x, y in zip(x_values, y_values):
        ax.text(x, y, f'{y:.2f}', ha='center', va='bottom', fontsize=8)

    ax.set_title('Trend of Energy Consumption')
    ax.set_xlabel('Year-Month')
    ax.set_ylabel('Energy Consumption Sum')
    ax.legend()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    img = base64.b64encode(buf.getbuffer()).decode("ascii")
    return img
@bp.route('/<int:id>/<int:sLid>/<int:deviceid>/panel', methods=('GET', 'POST'))
@login_required
def viewOrDeleteDevice(id, sLid, deviceid):
    year_image = None
    device = None
    activity_data = None
    if not isValidAccessDevice(id,sLid,deviceid):
        abort(403)
    if request.method == 'GET':
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'SELECT type, modelname, properties FROM device NATURAL JOIN model '
            'WHERE deviceid = %s',
            (deviceid,)
        )
        columns = [column[0] for column in cursor.description]
        res = cursor.fetchone()
        device = dict(zip(columns, res))
        cursor.execute(
            'SELECT year(timestamp) as year,month(timestamp) as month ,sum(value)  as total_energy'
            ' from device natural join datas '
            'WHERE deviceid = %s and eventLabel = "energy use" group by year(timestamp),month(timestamp)',
            (deviceid,)
        )
        columns = [column[0] for column in cursor.description]
        res = cursor.fetchall()
        if res is not None:
            year_data = [dict(zip(columns, row)) for row in res]
            year_image = plot_year_image(year_data)
        if len(res) == 0:
            year_image = None
        cursor.execute(
            'SELECT timestamp, eventLabel, ifnull(value ,0) as value '
            'from datas '
            'WHERE deviceid = %s and eventLabel <> "energy use" order by timestamp desc limit 5',
            (deviceid,)
        )
        columns = [column[0] for column in cursor.description]
        res = cursor.fetchall()
        if res is not None:
            activity_data = [dict(zip(columns, row)) for row in res]
        if len(res) == 0:
            activity_data = None
        #print(activity_data)

    return render_template('device/viewOrDeleteDevice.html', deviceid=deviceid,
                           id=id,sLid=sLid,device=device, plot_image=year_image, activity=activity_data)


@bp.route('/<int:id>/<int:sLid>/<int:deviceid>/delete', methods=('GET', 'POST'))
@login_required
def deleteDevice(id, sLid, deviceid):
    if not isValidAccessDevice(id,sLid,deviceid):
        abort(403)
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'DELETE FROM datas WHERE deviceid = %s',
        (deviceid,)
    )
    cursor.execute(
        'DELETE FROM device WHERE deviceid = %s',
        (deviceid,)
    )
    db.commit()
    return redirect(url_for('device.locationMain', id =id, sLid=sLid))
