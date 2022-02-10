# PythonRQR
Simple Reverse QR webapplication in python3 werkzeug/flask

This is a simple page that shows a QR code that allows for anyone to drop a text or link with nothing else.
It uses no database, only logging because... I guess I just felt like it.

Uses Redis for performance(or files for persistence) but will not have persistence.

Expected files for SSL:

- fullchain.pem
- privkey.pem
    
    
**TODO**
* ~~option without https~~
* ~~port number~~
* ~~vcenter QR code~~
* ~~better UI~~
* ~~WSGI~~
* expiration (date or views)
* ~~file upload~~
