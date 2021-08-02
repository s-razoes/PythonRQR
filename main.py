import ssl
import datetime
from flask import Flask, flash, render_template, request, redirect, send_from_directory
from werkzeug.serving import run_simple
import random
import os
import re

FILES_PATH = "DATA"
ID_SIZE = 30


def get_rnd_str(length):
    return ''.join(random.choices('1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=length))


def is_valid_idi(idi):
    if len(idi) != ID_SIZE:
        return False
    # check if idi has only numbers and alfa
    if len(re.findall("[0-9|A-z]", idi)) != ID_SIZE:
        return False
    return True


def load_file(idi, link=False):
    if link:
        file_path = os.path.join(FILES_PATH, idi, "link.txt")
        template = 'link.html'
    else:
        file_path = os.path.join(FILES_PATH, idi, "value.txt")
        template = 'read.html'

    f = open(file_path, "r")
    txt = f.read()

    if link:
        ltxt = txt.lower()
        if ltxt[:7] != "http://" and ltxt[:8] != "https://":
            txt = "https://" + txt
    return render_template(template, txt=txt)


FILES_PATH = os.path.join(os.getcwd(), FILES_PATH)


def main():
    app = Flask(__name__)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(filename='favicon.ico', directory="templates")

    @app.route('/', defaults={'path': None}, methods=['GET'])
    def home(path, message=''):
        while True:
            idi = get_rnd_str(ID_SIZE)
            path = os.path.join(FILES_PATH, idi)
            if os.path.exists(path) is False:
                return redirect("/" + idi, code=302)

    @app.route("/w/<string:idi>")
    def write(idi):
        if is_valid_idi(idi) is False:
            return "error"

        path = os.path.join(FILES_PATH, idi)
        if os.path.exists(path) is False:
            return "Not created"

        file_path = os.path.join(FILES_PATH, idi, "visitedW.txt")
        #if os.path.exists(file_path) is True:
        #    return "Already created"
        f = open(file_path, "a", encoding='utf8')
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        f.write(current_time + "\n")
        f.write(request.remote_addr + "\n")
        f.write(str(request.headers) + "\n")
        f.close()

        path = os.path.join(FILES_PATH, idi, "link.txt")
        if os.path.exists(path) is True:
            return "Already created"
        path = os.path.join(FILES_PATH, idi, "value.txt")
        if os.path.exists(path) is True:
            return "Already created"
        return render_template('write.html', qkey=idi)

    @app.route("/<string:idi>")
    def qr_host(idi):
        if is_valid_idi(idi) is False:
            return "error"

        path = os.path.join(FILES_PATH, idi, "link.txt")
        if os.path.exists(path) is True:
            return load_file(idi, link=True)
        path = os.path.join(FILES_PATH, idi, "value.txt")
        if os.path.exists(path) is True:
            return load_file(idi, link=False)
        
        folder = os.path.join(FILES_PATH, idi)
        if os.path.exists(folder) is False:
            print("Created folder: " + idi)
            os.mkdir(folder)
            
        file_path = os.path.join(folder, "created.txt")
        f = open(file_path, "a", encoding='utf8')
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        f.write(current_time + "\n")
        f.write(request.remote_addr + "\n")
        f.write(str(request.headers) + "\n")
        f.close()


        # return redirect("/" + idi, code=302)
        # render_template('home.html', qkey=generated_key)

        return render_template('home.html', qkey=idi)

    @app.route('/s', methods=['POST'])
    def store():
        txt = request.form['txt']
        idi = request.form['idi']
        type = request.form['type']
        if is_valid_idi(idi) is False or txt is None or txt == '':
            return "error"

        path = os.path.join(FILES_PATH, idi)

        file_value = os.path.join(FILES_PATH, idi, "value.txt")
        file_link = os.path.join(FILES_PATH, idi, "link.txt")
        if os.path.exists(path):
            if os.path.exists(file_link) or os.path.exists(file_value):
                return "already exists"
            f = None
            if type == "text":
                f = open(file_value, "a", encoding='utf8')
            elif type == "link":
                f = open(file_link, "a", encoding='utf8')
            f.write(txt)
            f.close()
        return redirect("/" + idi, code=302)

    @app.route("/c/<string:idi>")
    def check(idi):
        file_path = os.path.join(FILES_PATH, idi, "value.txt")
        if os.path.exists(file_path):
            return "1"
        file_path = os.path.join(FILES_PATH, idi, "link.txt")
        if os.path.exists(file_path):
            return "1"
        return "0"

    localIp = '0.0.0.0'
    port = 443

    ssl_context = None
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    crtFile = "fullchain.pem"
    keyFile = "privkey.pem"
    ssl_context.load_cert_chain(crtFile, keyFile)

    run_simple(localIp, port, app, ssl_context=ssl_context)


if __name__ == '__main__':
    main()
