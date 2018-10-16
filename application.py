#!/usr/bin/env python3.6

from autobahn.asyncio.component import Component
from autobahn.asyncio.component import run

component = Component(transports=u"ws://localhost:8080/ws", realm=u"realm1")

wamp_session = None

@component.on_join
async def join(session, details):
    print("session join")
    global wamp_session
    wamp_session = session
         
@component.on_leave
async def leave(session, reason):
    global wamp_session
    wamp_session = None
    print("session leave")
    
from switchio import Service, event_callback

class Application(object):
    @event_callback('CHANNEL_PARK')
    def on_park(self, session):
        if session.is_inbound():
            global wamp_session
            wamp_session.publish(u'call', session.host)
            session.hangup()

service = Service(['sipbox'])
service.apps.load_app(Application, app_id='default')
service.run(block=False)  

run([component])
