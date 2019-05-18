import logging
from flask import Flask, Blueprint, request
from flask_restplus import Api, Resource
from endpoints.contracts import contract_api
from endpoints.providers import provider_api

app = Flask(__name__)

app.register_blueprint(contract_api)
app.register_blueprint(provider_api)

@app.route("/")
def hello():
    app.logger.debug('HELLO!!!!!!!!!!')
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
else:
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
