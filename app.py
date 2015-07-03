#!flask/bin/python
import os
import csv
import uuid
from flask import Flask, request, redirect, url_for, abort, make_response, jsonify
from werkzeug import secure_filename
from dataapi import DataAPIS

dataAPI = DataAPIS()

UPLOAD_FOLDER = './uploads'
OUTPUT_FOLDER = './outputs'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def append_to_file(filepath,row):
    try:
        with open(filepath, 'ab') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
            writer.writerows(row)
            print 'writing'
    except Exception as e:
        print e
        abort(422)

def init_file(filepath):
    try:
        with open(filepath, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
            writer.writerows([['Email']])
            print 'file initialized'
    except Exception as e:
        print e
        abort(422)

def process_file(filepath,filename):
    print filepath
    try:
         output_file_path =  os.path.join(app.config['OUTPUT_FOLDER'], filename)
         init_file(output_file_path)
         with open(filepath) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
               email = row['Email']
               briteverify_response = dataAPI.briteverify(email)
               append_to_file(output_file_path,[[briteverify_response]])
    except Exception as e:
        print e
        abort(422)

@app.route('/')
def index():
    return "Welcome to Data Augmentation API"

#Here's the POST API To recieve and process the csv file
@app.route('/api',methods=['POST'])
def post_api():
        try:
            unique_name = str(uuid.uuid1())
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name+filename)
                file.save(filepath)
                process_file(filepath,unique_name+filename)
                return 'awesome'
            else:
                abort(422)
        except Exception as e:
            print e
            abort(422)



@app.errorhandler(422)
def not_found(error):
    return make_response(jsonify({'error': 'Invalid file or error in uploading the file. Please try again'}), 422)

if __name__ == '__main__':
    app.run(debug=True)
