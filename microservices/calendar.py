"""
Google Calendar manager, this service auth, create, edit and delete the events. 
The events are registered in biscenp@gmail.com but it will move to biscenfabian@gmail.com
By: EssEnemiGz
"""

from flask import *
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
import os.path
import pickle

calendar_bp = Blueprint('Google Calendar', __name__)

def credentials():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=6798)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def get_calendar(service):
    calendar_list = service.calendarList().list().execute().get('items', [])
    main_calendar = None
    for calendar in calendar_list:
        if calendar['summary'] == "biscenp@gmail.com": main_calendar = calendar
        
    if main_calendar == None: exit()
    return main_calendar
    
@calendar_bp.route("/api/calendar/add/event", methods=["PUT"])
def add_event():
    """
    Requested info: error_concept (resume), github_link, description, start (start date), end (end date)
    """
    
    service = credentials()
    main_calendar = get_calendar(service)
    
    data = request.get_json()
    if None in data.values():
        err = make_response( "Error, falta informacion" )
        err.status_code = 500
        return err
    
    resume = data.get("error_concept")
    github = data.get("github_link")
    description = data.get("description")
    
    # Admin info
    fecha_inicio = data.get("start")
    fecha_fin = data.get("end")
    
    event = {
        'summary': resume,
        'description': f'{description}\n\nRepository: {github}',
        'start': {
            'dateTime': (datetime.strptime(fecha_inicio, "%d-%m-%Y %H:%M")).isoformat(),
            'timeZone': 'America/Santo_Domingo',
        },
        'end': {
            'dateTime': (datetime.strptime(fecha_fin, "%d-%m-%Y %H:%M")).isoformat(),
            'timeZone': 'America/Santo_Domingo',
        },
    }
    
    service.events().insert(calendarId=main_calendar['id'], body=event).execute()
    
    response = make_response( "Event added to Google Calendar" )
    response.status_code = 200
    return response