from flask import Flask


from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)


@app.route('/healthz')
def health_check():
    return 'OK', 200


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8080)