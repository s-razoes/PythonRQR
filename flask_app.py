from flask import Flask, render_template, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
#project libraries
import config
import logger
import id_manager
import data_manager

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = config.MAX_FILE_SIZE * 1024 * 1024

@app.route('/qrcode.js')
def qrcode_js():
    return send_from_directory(path='qrcode.js', directory="templates")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path='favicon.ico', directory="templates")

@app.route('/', defaults={'path': None}, methods=['GET'])
def home(path, message=''):
    idi = id_manager.create_id()
    return redirect("/" + idi, code=302)

@app.route("/w/<string:idi>")
def write(idi):
    if id_manager.is_valid_id(idi) is False:
        return "error"

    if id_manager.id_created(idi) is False:
        return "Not created"

    logger.log_call(request, idi, "Call for write")

    if id_manager.id_has_content(idi):
        return "Already created"

    id_manager.setup_id(idi, request.remote_addr + "\n" + str(request.headers))

    return render_template('write.html', qkey=idi)

@app.route("/<string:idi>")
def qr_host(idi):
    if id_manager.is_valid_id(idi) is False:
        return "error"

    logger.log_call(request, idi, "Read")

    content_type = data_manager.id_type(idi)
    if content_type in (config.CONTENT_TYPE.LINK,config.CONTENT_TYPE.VALUE,config.CONTENT_TYPE.FILE):
        data, valData = data_manager.load_data(idi, content_type)
        if content_type is config.CONTENT_TYPE.FILE:
            response = make_response(data)
            response.headers.set('Content-Disposition', 'attachment', filename=valData)
            return response
        if content_type == config.CONTENT_TYPE.LINK:
            template = 'link.html'
        else:
            template = 'read.html'
        return render_template(template, txt=valData)

    return render_template('home.html', qkey=idi, MAX_CONTENT_LENGTH=config.MAX_FILE_SIZE)

@app.route('/s', methods=['POST'])
def store():
    txt = request.form['txt']
    idi = request.form['idi']
    type = request.form['type']
    if id_manager.is_valid_id(idi) is False or txt is None or txt == '':
        return "error"

    if id_manager.id_has_content(idi):
        return "Already exists!"

    logger.log_call(request, idi, "Write")

    data_manager.write_data(idi, txt, type)

    return render_template('finished.html')

@app.route('/f', methods=['POST'])
def file_store():
    idi = request.form['idi']
    if id_manager.is_valid_id(idi) is False:
        return "error"

    if id_manager.id_has_content(idi):
        return "Already exists!"

    if 'file' not in request.files:
        return 'No file.'
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    logger.log_call(request, idi, "Write file")

    data_manager.write_data(idi, file, config.CONTENT_TYPE.FILE, filename)

    return render_template('finished.html')


@app.route("/c/<string:idi>")
def check(idi):
    if id_manager.is_id_setup(idi):
        if id_manager.id_has_content(idi):
            return "2" #finished uploading value
        return "1" #only setup
    return "0"
