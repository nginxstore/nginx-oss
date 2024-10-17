import os
from flask import Flask, request, redirect, url_for, render_template_string, flash, send_file

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')

def allowed_file(filename):
    return '.' in filename

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def browse_directory(path):
    full_path = os.path.join(app.config['UPLOAD_FOLDER'], path)

    if not os.path.exists(full_path):
        flash('경로를 찾을 수 없습니다.')
        return redirect(url_for('browse_directory'))

    if os.path.isfile(full_path):
        return send_file(full_path, as_attachment=True)

    files = os.listdir(full_path)
    file_list = ''.join(
        f'<li><a href="/{os.path.join(path, filename)}">{filename}/</a></li>' if os.path.isdir(os.path.join(full_path, filename)) 
        else f'<li><a href="/{os.path.join(path, filename)}">{filename}</a></li>'
        for filename in files
    )

    return render_template_string('''
    <!doctype html>
    <title>Download server</title>
    <h2>파일 다운로드</h2>
    <ul>
      {{ file_list|safe }}
    </ul>
    ''', file_list=file_list)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  
    app.run(host='0.0.0.0', port=8081)
