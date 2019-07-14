import os, json, requests
from flask import Flask, url_for, render_template, request, jsonify

from blueprints import providers, contracts, projects, follow_ups, catalogs, graphics


app = Flask(__name__)

app.register_blueprint( providers.bp )
app.register_blueprint( contracts.bp )
app.register_blueprint( projects.bp )
app.register_blueprint( follow_ups.bp )
app.register_blueprint( catalogs.bp )
app.register_blueprint( graphics.bp )




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
