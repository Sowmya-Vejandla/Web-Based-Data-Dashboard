# Program to create a web based dashboard using python


from flask import Flask, redirect, render_template, request, jsonify
import os
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Routing the home() to render the home.html
@app.route('/')
def home():
    return render_template('home.html')

# Routing the upload_file() to render the index.html with all datasets
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect('/')
    files = request.files.getlist('file')

    for file in files:
        if file and file.filename.endswith(('.csv', '.xlsx')):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
    datasets = os.listdir(app.config['UPLOAD_FOLDER'])

    return render_template('index.html', datasets=datasets)


@app.route('/analyze',methods=['POST'])
# Function to get the each dataset with required information
def analyze():
    file_name = request.form['file_name']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    data =pd.read_csv(file_path)
    print(data.head())
   

    columns = data.columns.tolist()
    data_summary = {
        'columns': columns,
        'types': data.dtypes.astype(str).tolist(),
        'sample_data': data.head(10).to_dict(orient='records')
    }
    return jsonify(data_summary)

if __name__ == '__main__':
    app.run(debug=True) # Running the flask app