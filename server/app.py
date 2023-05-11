from flask import Flask, g, make_response, jsonify, request
from datetime import datetime, date, timedelta
from db import Database, Vaccination, Client, Covid19, ERROR, OK, Image
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.db = Database()


@app.route('/')
def home():
    return 'Welcome to the homepage!'



@app.route('/get/client/<int:client_id>')
def get_client(client_id):
    """Get client by id"""
    client = app.db.get_client_by_id(client_id)
    if client:
        response = make_response(jsonify(client.__dict__), OK)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response('Client not found.', ERROR)
        return response



@app.route('/get/vaccines_list/<int:client_id>')
def get_vaccines_list(client_id):
    """Get vaccines list by id"""
    client = app.db.get_client_by_id(client_id)
    if client:
        vaccines_list: list = app.db.get_vaccines_list_by_id(client_id)
        #   response_data = [Vaccination.__dict__ for vaccines in vaccines_list]
        response = make_response(jsonify(vaccines_list), 201)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response('Client not found.', ERROR)
        return response



@app.route('/covid/info/<int:client_id>')
def get_covid_info(client_id):
    """Get covid19  info by id"""
    client: Client = app.db.get_client_by_id(client_id)
    if client:
        covid: Covid19 = app.db.get_covid_info_by_id(client_id)
        if covid:
            response = make_response(jsonify(covid.__dict__), OK)
            response.headers['Content-Type'] = 'application/json'
            return response
        response = make_response('No covid19 information exist.', ERROR)
        return response
    else:
        response = make_response('Client not found.', ERROR)
        return response


@app.route('/add_client', methods=['POST'])
def add_client():
    """dd a new client"""
    json_data = request.get_json()
    new_client = None
    try:
        new_client = Client(**json_data)
        new_client.client_id = int(new_client.client_id)
        if not (valid_date(new_client.born_date)):
            return make_response('The date of birth was not yet', ERROR)
    except Exception as error:
        print(error)
        response = make_response('Invalid values', ERROR)
        return response
    if app.db.client_exists(new_client.client_id):
        return make_response('A client with such an ID already exists', ERROR)
    else:
        app.db.add_client(new_client)
        return make_response('Client successfully  added', OK)


@app.route('/add_vaccine', methods=['POST'])
def add_vaccine():
    """Add a vaccine for client"""
    json_data = request.get_json()
    if 'client_id' in json_data and 'manufacturer' in json_data and 'date' in json_data:
        if not app.db.client_exists(int(json_data['client_id'])):
            return make_response('Client not found.', ERROR)
        client: Client = app.db.get_client_by_id(int(json_data['client_id']))
        if len(app.db.get_vaccines_list_by_id(client.client_id)) == 4:
            return make_response('The client already has 4 vaccinations.', ERROR)
        if not (json_data['date']):
            return make_response('The date of vaccination was not yet', ERROR)
        if not valid_date(client.born_date, json_data['date']):
            return make_response('The vaccination date cannot be before the birth date.', ERROR)
        if not valid_vaccination(client.client_id, json_data['date']):
            return make_response('The vaccination date is within 14 days of an already reported vaccination date.', ERROR)
        result = app.db.add_vaccine(client.client_id, json_data['manufacturer'], json_data['date'])
        if result == ERROR:
            return make_response('Server error.', ERROR)
        else:
            return make_response('Vaccine successfully added.', OK)
    else:
        return make_response('Invalid values', ERROR)


@app.route('/add_covid', methods=['POST'])
def add_covid():
    """Add covid for client"""
    json_data = request.get_json()
    new_covid = None
    try:
        new_covid = Covid19(**json_data)
        new_covid.client_id = int(new_covid.client_id)
    except Exception as error:
        response = make_response('Invalid values', ERROR)
        return response
    if not (app.db.client_exists(new_covid.client_id)):
        return make_response('Client not found.', ERROR)
    else:
        birth_date = app.db.get_client_by_id(new_covid.client_id).born_date
        if not (valid_date(new_covid.positive_date)):
            return make_response('The positive date was not yet', ERROR)
        if not valid_date(birth_date, new_covid.recovery_date):
            return make_response('The recovery date cannot be before the birth date.', ERROR)
        if not valid_date(birth_date, new_covid.positive_date):
            return make_response('The positive date date cannot be before the birth date.', ERROR)
        if not valid_date(new_covid.positive_date, new_covid.recovery_date):
            return make_response('The recovery date date cannot be before the positive date.', ERROR)
        result = app.db.add_covid(new_covid)
        if result == ERROR:
            return make_response('A disease cannot be added twice.', ERROR)
        else:
            return make_response('The details successfully added.', OK)


@app.route('/vaccine/data', methods=['GET'])
def get_data():
    data = app.db.vaccine_info()
    return jsonify(data)


@app.route('/upload', methods=['POST'])
def upload():
    if 'image' in request.files:
        image = request.files['image']
        client_id = request.form['client_id']
        if not (app.db.client_exists(client_id)):
            return make_response('Client not found.', ERROR)
        img_name = request.form['img_name']
        new_img = Image(client_id, img_name, image.bytes)
        result = app.db.add_image(new_img)
        if result == ERROR:
            return make_response('Server error.', ERROR)
        return make_response('Image uploaded successfully', OK)
    else:
        response = make_response('Invalid values', ERROR)
        return response


def valid_date(date_1, date_2=datetime.now()):
    """Returns true if date_1 was before date_2"""
    if isinstance(date_1, str):
        date_1 = datetime.strptime(date_1, '%d/%m/%Y')
    if isinstance(date_2, str):
        date_2 = datetime.strptime(date_2, '%d/%m/%Y')
    return date_1 < date_2


def valid_vaccination(client_id, vaccine_date) -> bool:
    """Returns true if the new vaccine date is legal (not within 14 days from all the reported vaccinations)"""
    vaccine_date = datetime.strptime(vaccine_date, '%d/%m/%Y')
    vaccination_list = app.db.get_vaccines_list_by_id(client_id)
    for vaccine in vaccination_list:
        delta = abs(vaccine_date - datetime.strptime(vaccine.date, '%d/%m/%Y'))
        if delta < timedelta(days=14) and date != 0 :
            return False
    return True
