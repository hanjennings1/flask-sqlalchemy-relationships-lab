#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# TODO: add functionality to all routes

@app.route('/events')
def get_events():
    events = Event.query.all()      # get all events from the database

    events_list = []                # will hold each event as a dict
    for event in events:
        events_list.append({
            "id": event.id,
            "name": event.name,
            "location": event.location,
        })

    return jsonify(events_list), 200    # send list as JSON with 200 OK status


@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    event = Event.query.filter_by(id=id).first()  # find event by id (None if missing)

    if not event:
        return jsonify({"error": "Event not found"}), 404  # stop here if no event

    sessions_list = []          # will hold each session as a dict
    for s in event.sessions:    # use the one-to-many relationship
        sessions_list.append({
            "id": s.id,
            "title": s.title,
            "start_time": s.start_time.isoformat(),  # convert datetime to a JSON-friendly string
        })

    return jsonify(sessions_list), 200  # send list as JSON with 200 OK status


@app.route('/speakers')
def get_speakers():
    speakers = Speaker.query.all()      # get all speakers from the database

    speakers_list = []                  # will hold each speaker as a dict
    for speaker in speakers:
        speakers_list.append({
            "id": speaker.id,
            "name": speaker.name,
        })

    return jsonify(speakers_list), 200  # send list as JSON with 200 OK status


@app.route('/speakers/<int:id>')
def get_speaker(id):
    pass


@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    pass


if __name__ == '__main__':
    app.run(port=5555, debug=True)
