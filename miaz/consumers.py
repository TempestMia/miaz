from django.conf import settings
import re
import json
import logging
import datetime
from channels import Group
from channels.sessions import channel_session
from molten.models import World

log = logging.getLogger(__name__)

@channel_session
def ws_connect(message):
    # Extract the world from the message. This expects message.path to be of the
    # form /chat/{label}/, and finds a World if the message path is applicable,
    # and if the World exists. Otherwise, bails (meaning this is a some othersort
    # of websocket). So, this is effectively a version of _get_object_or_404.
    try:
        chat = message.get('path')
        label = 'auto123'
        if chat != '/chat':
            print('invalid ws path=%s', message['path'])
            return
        world = World.objects.get(label=label)
    except ValueError:
        print('invalid ws path=%s', message['path'])
        return
    except World.DoesNotExist:
        print('ws world does not exist label=%s', label)
        return

    print('chat connect world=%s client=%s:%s',
        world.label, message['client'][0], message['client'][1])
    
    # Need to be explicit about the channel layer so that testability works
    # This may be a FIXME?
    print dir(message)
    print "channel: ",message.channel
    print "channel_layer: ", message.channel_layer
    print "content: ", message.content
    print "reply_channel: ", message.reply_channel
    Group('chat-'+label, channel_layer=message.channel_layer).add(message.reply_channel)

    message.channel_session['world'] = world.label

@channel_session
def ws_receive(message):
    print 'message text ', message.get('text')
    # Look up the world from the channel session, bailing if it doesn't exist
    try:
        label = message.channel_session['world']
        world = World.objects.get(label=label)
    except KeyError:
        print('no world in channel_session')
        return
    except World.DoesNotExist:
        print('received message, but room does not exist label=%s', label)
        return

    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.
    try:
        data = json.loads(message['text'])
    except ValueError:
        # log.debug("ws message isn't json text=%s", text) # MZ: found undeclared var
        print("ws message isn't json text=%s", message['text'])
        return
    
    if set(data.keys()) != set(('handle', 'message')):
        log.debug("ws message unexpected format data=%s", data)
        return

    if data:
        print('chat message world=%s handle=%s message=%s',
            world.label, data['handle'], data['message'])
        m = world.messages.create(**data)

        # MZ: I can't serialize the datetime of the object so I'll make a dict myself, fuck.
        json_message = {
            'handle': m.handle,
            'message': m.message,
            'timestamp': m.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }

        # See above for the note about Group
        try:
            Group('chat-'+label, channel_layer=message.channel_layer).send({'text': json.dumps(json_message)})
        except StandardError as e:
            print 'Errrror:', e

@channel_session
def ws_disconnect(message):
    print "DISCONNECTING"
    try:
        label = message.channel_session['world'] # MZ: 'room' should be world?
        world = World.objects.get(label=label)
        Group('chat-'+label, channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, World.DoesNotExist) as e:
        print e
        pass
