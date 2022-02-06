import ssl
from flask import Flask, flash, render_template, request, redirect, send_from_directory
from werkzeug.serving import run_simple
import os.path
#project libraries
import config
import logger
import id_manager
import data_manager


def main():
    app = Flask(__name__)

    @app.route('/qrcode.js')
    def qrcode_js():
        return send_from_directory(filename='qrcode.js', directory="templates")

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(filename='favicon.ico', directory="templates")

    @app.route('/', defaults={'path': None}, methods=['GET'])
    def home(path, message=''):
        idi = id_manager.create_idi()
        return redirect("/" + idi, code=302)

    @app.route("/w/<string:idi>")
    def write(idi):
        if id_manager.is_valid_idi(idi) is False:
            return "error"

        if id_manager.id_created(idi) is False:
            return "Not created"

        logger.log_call(request, idi, "Call for write")

        if id_manager.id_has_lnk_val(idi):
            return "Already created"

        return render_template('write.html', qkey=idi)

    @app.route("/<string:idi>")
    def qr_host(idi):
        if id_manager.is_valid_idi(idi) is False:
            return "error"

        #id_manager.create_id(idi)
        logger.log_call(request, idi, "Read")

        link_value = id_manager.id_link_value(idi)
        if link_value in ('1','2'):
            lnk = (link_value == '1')
            data = data_manager.load_data(idi, link=lnk)
            if lnk:
                template = 'link.html'
            else:
                template = 'read.html'
            return render_template(template, txt=data)

        return render_template('home.html', qkey=idi)

    @app.route('/s', methods=['POST'])
    def store():
        txt = request.form['txt']
        idi = request.form['idi']
        type = request.form['type']
        if id_manager.is_valid_idi(idi) is False or txt is None or txt == '':
            return "error"

        if id_manager.id_has_lnk_val(idi):
            return "already exists!"

        logger.log_call(request, idi, "Write")

        data_manager.write_data(idi, txt, type)

        return redirect("/" + idi, code=302)

    @app.route("/c/<string:idi>")
    def check(idi):
        if id_manager.id_has_lnk_val(idi):
            return "1"
        return "0"

    port = 80
    ssl_context = None

    if config.secure:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.load_cert_chain(crtFile, keyFile)
        port = 443

    if config.defaultPort is not None:
        port = config.defaultPort

    run_simple(config.localIp, port, app, ssl_context=ssl_context)


if __name__ == '__main__':
    main()
