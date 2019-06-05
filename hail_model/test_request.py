import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import model.apply_model as am


UPLOAD_FOLDER = '/Users/Fabian/Projects/HackBay2019/hail_model/request_data'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

#def allowed_file(filename):
#    return '.' in filename and \
#           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/output_data', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('results',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
@app.route('/results', methods=['GET', 'POST'])
def results():
   # output = am.apply_model(test_dir=UPLOAD_FOLDER+'/', test_dir_resized=UPLOAD_FOLDER+'_resized/')
    #redirect(url_for('results',filename=filename))
    return am.apply_model(test_dir=UPLOAD_FOLDER+'/', test_dir_resized=UPLOAD_FOLDER+'_resized/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

















"""
from flask import Flask, request, abort

app = Flask(__name__)


@app.route('/output_data', methods=['POST']) 
def foo():
    print(request)
    file = request.files['']
    print(file)
    return "he4llo"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
"""