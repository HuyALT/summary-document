from viSummary import summary
from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from docx import Document
from flask_cors import CORS

app = Flask(__name__) # Khởi tạo ứng dụng
CORS(app) # Cho phép gọi Api từ server
app.config['UPLOAD_FOLDER'] = 'uploads' # Tạo folder chứa file tải lên
ALLOWED_EXTENSIONS = {'txt', 'docx'} # tạo danh sách các tệp cho pép

# kiểm tra tệp có thuộc định dạng cho phép hay không
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/summary', methods=['POST'])
def summaryData():
    json_data = request.get_json() # Nhận JSON
    contents = json_data.get('contents') # Lấy dữ liệu contents trong JSON
    if not contents:
        return jsonify({'error': 'Missing data'}), 400
    response = {
        'message':'Sucessful',
        'summaryData': summary(contents) # Gọi hàm tóm tắt văn bản
    }
    return response

@app.route('/api/getfiledata', methods=['POST'])
def getfilecontents():
    file = request.files.get('file') # Lấy file đuơc gửi lên

    filename = secure_filename(file.filename) # kiểm tra file có an toàn hay không
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename) #Lưu file vào tệp
    file.save(filepath)

    file_content = ""
    # kiểm tra đuôi file để có cách xử lý khác nhau
    if filename.endswith('.txt'):
        with open(filepath, 'r', encoding='utf-8') as f:
            file_content = f.read()
    elif filename.endswith('.docx'):
        doc = Document(filepath)
        file_content = "\n".join([para.text for para in doc.paragraphs])

    response = {
        'message': 'Sucessful',
        'data': file_content
    }
    return response

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True, port=8080)
