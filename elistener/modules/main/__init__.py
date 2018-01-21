import re
import logging
import requests

from elistener import app
from elistener import connect_db

from flask import g
from flask import abort
from flask import request
from flask import jsonify
from flask import Blueprint


main = Blueprint('main', __name__)

elistener_logger = logging.getLogger('eListener')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'mongo_db'):
        g.mongo_client, g.mongo_db = connect_db()
    return g.mongo_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'mongo_db'):
        if g.mongo_client is not None:
            g.mongo_client.close()


@main.route('/api/facebook', methods=['GET', 'POST'])
def facebook():
    # elistener_logger.error(request)
    elistener_logger.error(request.json)
    config = app.config
    # Facebook Challenge
    if request.method == 'GET':
        hub_mode = request.args.get('hub.mode', '')
        hub_verify_token = request.args.get('hub.verify_token', '')
        hub_challenge = request.args.get('hub.challenge', '')
        if hub_mode == 'subscribe' and hub_verify_token == config["FB_HUB_VERIFY_TOKEN"]:
            return hub_challenge
        else:
            abort(403)
    elif request.method == 'POST':
        data = request.json
        db = get_db()
        msg_json = {
            "status": 0,
            "source": "facebook",
            "data": data
        }
        inserted_id = db["db_raw_input"]["raw_input"].insert_one(msg_json).inserted_id
        if not inserted_id:
            abort(500)
    return jsonify({})


@main.route('/api/telegram', methods=['POST'])
def telegram():
    data = request.json
    db = get_db()
    msg_json = {
        "status": 0,
        "source": "telegram",
        "data": data
    }
    inserted_id = db["db_raw_input"]["raw_input"].insert_one(msg_json).inserted_id
    if not inserted_id:
        abort(500)
    return jsonify({})
