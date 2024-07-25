from main import app
from dbConfig import mysql
import MySQLdb.cursors
from flask import Flask, jsonify, request
from datetime import datetime


@app.route('/show')
def showBookings():
    cursor = None
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        selectQuery = 'select * from bookings'
        cursor.execute(selectQuery)
        result = cursor.fetchall()
        response = jsonify(result)
        response.status_code = 200
        return response
    except Exception as error:
        print(error)
    finally:
        if cursor is not None:
            cursor.close()


@app.route('/show/<int:id>')
def showById(id):
    cursor = None
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        selectByIdQuery = 'SELECT * FROM bookings where id = %s'
        cursor.execute(selectByIdQuery, (id,))
        result = cursor.fetchone()
        if result:
            response = jsonify(result)
            response.status_code = 200
        else:
            response = jsonify({'error': 'Record not found'})
            response.status_code = 404

        return response
    except Exception as error:
        print(error)
        response = jsonify({'error': str(error)})
        response.status_code = 500
        return response
    finally:
        if cursor is not None:
            cursor.close()


@app.route('/addPassenger',  methods=['POST'])
def addData():
    cursor = None
    try:
        _json = request.get_json()
        _name = _json['name']
        _age = _json['age']
        _noOfBookings = _json['noOfBookings']

        if _name and _age and _noOfBookings and request.method == 'POST':
            insertQuery = '''INSERT INTO bookings(name, age, noOfBookings, dateOfBooking, price)
                             VALUES(%s, %s, %s, %s, %s)'''
            _date = datetime.now().date()
            if _age > 60:
                _price = 750 + (_noOfBookings - 1)*1500
            else:
                _price = 1500 * _noOfBookings
            values = (_name, _age, _noOfBookings, _date, _price)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(insertQuery, values)
            mysql.connection.commit()
            response = jsonify({'message': 'Booking created successfully'})
            response.status_code = 201
            return response
        else:
            return jsonify('Invalid Inputs')

    except Exception as error:
        print(error)
        response = jsonify({'error': str(error)})
        response.status_code = 500
        return response
    finally:
        if cursor is not None:
            cursor.close()


@app.route('/updatePassenger/<int:id>', methods=['PATCH'])
def updateData(id):
    cursor = None
    try:
        _json = request.get_json()
        _noOfBookings = _json['noOfBookings']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        selectQuery = 'SELECT noOfBookings, price from bookings WHERE id = %s'
        cursor.execute(selectQuery, (id, ))
        passengerData = cursor.fetchone()
        if passengerData is None:
            response = jsonify({'message': 'Could not find the Booking'})
            response.status_code = 404
            return response
        else:
            oldNoOfBookings = passengerData['noOfBookings']
            oldPrice = passengerData['price']
            priceDifference = (_noOfBookings - oldNoOfBookings) * 1500
            finalPrice = oldPrice + priceDifference
            if _noOfBookings and request.method == 'PATCH':
                updateQuery = 'UPDATE bookings SET noOfBookings = %s, price = %s WHERE id = %s'
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(updateQuery, (_noOfBookings, finalPrice, id))
                mysql.connection.commit()
                response = jsonify({'message': 'Bookings updated successfully'})
                response.status_code = 202
                return response
            else:
                return jsonify('Invalid Inputs')

    except Exception as error:
        print(error)
        response = jsonify({'error': str(error)})
        response.status_code = 500
        return response
    finally:
        if cursor is not None:
            cursor.close()


@app.route('/deletePassenger/<int:id>', methods=['DELETE'])
def deleteData(id):
    cursor = None
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        selectQuery = 'SELECT noOfBookings, price from bookings WHERE id = %s'
        cursor.execute(selectQuery, (id, ))
        passengerData = cursor.fetchone()
        if passengerData is None:
            response = jsonify({'message': 'Could not find the Bookings'})
            response.status_code = 404
            return response
        else:
            if request.method == 'DELETE':
                deleteQuery = 'DELETE FROM bookings  WHERE id = %s'
                cursor.execute(deleteQuery, (id,))
                mysql.connection.commit()
                response = jsonify({'message': 'Booking deleted successfully'})
                response.status_code = 204
                return response
            else:
                return jsonify('Invalid Route')

    except Exception as error:
        print(error)
        response = jsonify({'error': str(error)})
        response.status_code = 500
        return response
    finally:
        if cursor is not None:
            cursor.close()


if __name__ == '__main__':
    app.run(debug=True)



