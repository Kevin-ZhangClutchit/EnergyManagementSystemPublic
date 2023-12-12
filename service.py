import functools
import mysql.connector
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import current_user

from flaskr.auth import login_required
from flaskr.db import get_db
from werkzeug.exceptions import abort

bp = Blueprint('service', __name__, url_prefix='/service')
from flask_login import current_user


def isValidAccess(id):
    return current_user.id == id


def isValidAccessSLid(id, sLid):
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


@bp.route('/<int:id>/main')
@login_required
def userMain(id):
    if not isValidAccess(id):
        abort(403)
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'SELECT servicelocation.SLid as sLid, addr, zipcode, unitNumber, tookOverDate, squareFootage, bedroomCnt, occupantsCnt'
        ' FROM user natural join customer_service natural join servicelocation'
        ' WHERE user.cid = %s ORDER BY sLid',
        (id,)
    )
    columns = [column[0] for column in cursor.description]
    serviceLocs = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return render_template('service/userMain.html', serviceLocs=serviceLocs)


def get_serviceLoc(sLid, check_user=True):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'SELECT cid , addr, zipcode, unitNumber, tookOverDate, squareFootage, bedroomCnt, occupantsCnt'
        ' FROM customer_service NATURAL JOIN servicelocation'
        ' WHERE sLid = %s',
        (sLid,)
    )
    columns = [column[0] for column in cursor.description]
    res = cursor.fetchone()
    res_dict = dict(zip(columns, res))
    serviceLoc = res_dict
    if serviceLoc is None:
        abort(404, f"Service Location id {sLid} doesn't exist.")

    if check_user and serviceLoc["cid"] != current_user.id:
        abort(403)
    return serviceLoc


@bp.route('/<int:id>/addLocation', methods=('GET', 'POST'))
@login_required
def addLocation(id):
    if not isValidAccess(id):
        abort(403)
    if request.method == 'POST':
        addr = request.form['addr']
        zipcode = request.form['zipcode']
        unitNumber = request.form['unitNumber']
        squareFootage = request.form['squareFootage']
        bedroomCnt = request.form['bedroomCnt']
        occupantsCnt = request.form['occupantsCnt']
        error = None

        if not addr or not zipcode or not unitNumber or not squareFootage or not bedroomCnt \
                or not occupantsCnt:
            error = 'A required field is empty.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO servicelocation (addr, zipcode, unitNumber, tookOverDate, squareFootage, bedroomCnt, occupantsCnt)'
                ' VALUES (%s, %s, %s, NOW(), %s, %s, %s)',
                (addr, zipcode, unitNumber, squareFootage, bedroomCnt, occupantsCnt,)
            )
            cursor.execute("SELECT LAST_INSERT_ID()")
            sLid = cursor.fetchone()[0]

            cursor.execute(
                'INSERT INTO customer_service (cid, sLid)'
                ' VALUES (%s, %s)',
                (id, sLid)
            )
            db.commit()
            return redirect(url_for('service.userMain', id=id))

    return render_template('service/addLocation.html')


@bp.route('/<int:id>/<int:sLid>/update', methods=('GET', 'POST'))
@login_required
def editLocation(id, sLid):
    if not isValidAccessSLid(id, sLid):
        abort(403)
    serviceLoc = get_serviceLoc(sLid)

    if request.method == 'POST':
        addr = request.form['addr']
        zipcode = request.form['zipcode']
        unitNumber = request.form['unitNumber']
        squareFootage = request.form['squareFootage']
        bedroomCnt = request.form['bedroomCnt']
        occupantsCnt = request.form['occupantsCnt']
        error = None

        if not addr or not zipcode or not unitNumber or not squareFootage or not bedroomCnt \
                or not occupantsCnt:
            error = 'A required field is empty.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'UPDATE servicelocation SET addr = %s, zipcode = %s, unitNumber = %s,'
                ' squareFootage = %s, bedroomCnt = %s, occupantsCnt = %s'
                ' WHERE sLid = %s',
                (addr, zipcode, unitNumber, squareFootage, bedroomCnt, occupantsCnt, sLid)
            )
            db.commit()
            return redirect(url_for('service.userMain', id=current_user.id))
    else:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'select count(*) as count from device'
            ' WHERE sLid = %s',
            (sLid,)
        )
        count = cursor.fetchone()[0]

    return render_template('service/editLocation.html', serviceLoc=serviceLoc, sLid=sLid, count=count)


@bp.route('/<int:id>/<int:sLid>/delete', methods=('GET', 'POST'))
@login_required
def deleteLocation(id, sLid):
    # serviceLoc=get_serviceLoc(sLid)
    if not isValidAccessSLid(id, sLid):
        abort(403)
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM customer_service WHERE cid = %s AND sLid = %s', (id, sLid,))
    cursor.execute('DELETE FROM servicelocation WHERE sLid = %s', (sLid,))
    db.commit()
    return redirect(url_for('service.userMain', id=id))
