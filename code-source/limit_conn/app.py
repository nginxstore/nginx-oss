from flask import Flask, request, redirect, url_for, render_template_string, flash, send_file
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')

def allowed_file(filename):
    return '.' in filename

@app.route('/', methods=['GET', 'POST'])
def root_page():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    file_list = ''.join(f'<li><a href="/file/{filename}">{filename}</a></li>' for filename in files)
    
    return render_template_string('''
    <!doctype html>
    <title>Download server</title>
    <h2>업로드된 파일</h2>
    <ul>
      {{ file_list|safe }}
    </ul>
    ''', file_list=file_list)

@app.route('/file/<filename>')
def get_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if os.path.isfile(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        flash('파일을 찾을 수 없습니다.')
        return redirect(url_for('upload_file'))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  
    app.run(host='0.0.0.0', port=8081)