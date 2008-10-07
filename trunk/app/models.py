from cgi import escape
from google.appengine.ext import db


class GameSeed(db.Model):
    originator = db.UserProperty(required=True)
    name = db.StringProperty(required=True)
    URL = db.LinkProperty(required=True)
    creation_time = db.DateTimeProperty(auto_now_add=True)


class Card(db.Model):
    gameseed = db.ReferenceProperty(GameSeed, required=True)
    sender = db.UserProperty(required=True)
    recipient = db.UserProperty(required=True)
    seen = db.BooleanProperty(default=False)
    creation_time = db.DateTimeProperty(auto_now_add=True)


def gameSeedFragment(gameseed, send=''):
    if send:
        send = '<a href=/createcard/%s>send this</a><br>' \
               % str(gameseed.key())
    return ('''<div><strong>GameSeed: %(name)s</strong><br>
%(send)s
Created by %(originator)s, <a href=%(URL)s>link</a>
</div>
''') % dict(
    originator = gameseed.originator.nickname(),
    send = send,
    name = escape(gameseed.name),
    URL = gameseed.URL,
    )


def gameSeedOneLiner(gameseed):
    return ('''<div><em><a href=/gameseed/%(gameseed_URL)s>'''
            '''GameSeed: %(name)s</a></em>
<a href=/createcard/%(gameseed_URL)s>send</a>
Created by %(originator)s, <a href=%(URL)s>view gameseed's webpage</a>
</div>
''') % dict(
    name = escape(gameseed.name),
    gameseed_URL = str(gameseed.key()),
    originator = gameseed.originator.nickname(),
    URL = gameseed.URL,
    )


def cardFragment(card):
    return ('''<div><h3>Card for <a href=/gameseed/%(gameseed_URL)s>'''
            '''GameSeed: %(gameseed_name)s</a></h3>
from %(sender)s, to %(recipient)s, %(seen)s
</div>
''') % dict(
    sender = card.sender.nickname(),
    recipient = card.recipient.nickname(),
    seen = ('unseen', 'seen')[card.seen],
    gameseed_name = card.gameseed.name,
    gameseed_URL = str(card.gameseed.key()),
    )


def cardOneLiner(card):
    return ('''<div><em><a href=/card/%(card_URL)s>'''
            '''Card: %(card_URL)s</a></em> for
<a href=/gameseed/%(gameseed_URL)s>GameSeed: %(gameseed_name)s</a>
from %(sender)s, to %(recipient)s, %(seen)s
</div>
''') % dict(
    card_URL = str(card.key()),
    gameseed_name = escape(card.gameseed.name),
    gameseed_URL = str(card.gameseed.key()),
    sender = card.sender.nickname(),
    recipient = card.recipient.nickname(),
    seen = ('unseen', 'seen')[card.seen],
    )


##def cardOneLiner(card):
##    return ('''<div><em><a href=/card/%(card_URL)s>'''
##            '''Card: %(card_URL)s</a></em> for
##<a href=/gameseed/%(gameseed_URL)s>GameSeed: %(gameseed_name)s</a>
##from %(sender)s, to %(recipient)s, %(seen)s
##</div>
##''') % dict(
##    card_URL = str(card.key()),
##    gameseed_name = escape(card.gameseed.name),
##    gameseed_URL = str(card.gameseed.key()),
##    sender = card.sender.nickname(),
##    recipient = card.recipient.nickname(),
##    seen = ('unseen', 'seen')[card.seen],
##    )


