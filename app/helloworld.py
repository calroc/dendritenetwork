'''
This is a basic prototype of the Dendrite Network system.
'''
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import users
from models import (
    DendriteNode,
    GameSeed,
    Card,
    gameSeedFragment,
    gameSeedOneLiner,
    cardFragment,
    cardOneLiner,
    )


dbGet = lambda key: db.get(db.Key(key))
# Given a db key, dig out its data from the db.


def getDendriteNode(uid):
    '''
    Given a UID return that user's DendriteNode or None if there's no
    such DN in the db.
    '''
    if uid is None: return
    uid = int(uid)
    q = DendriteNode.all().filter('uid =', uid)
    r = q.fetch(1)
    return (r and r[0]) or None


class GameSeedHandler(webapp.RequestHandler):
    '''
    Handles creation of GameSeed objects.

    GET returns a form for creating a new GameSeed, and POST handles
    receiving the results of that form.
    '''

    _seedCreationForm = '''\
<form action="/creategameseed" method="post">
  Your UID:<input type="text" name="uid"><br>
  GameSeed Name:<input type="text" name="name"><br>
  GameSeed URL:<input type="text" name="URL" size=128><br>
  <input type="submit" value="Create new GameSeed">
</form>'''

    def get(self):
        self.response.out.write(
            '<html><body>%s</body></html>' % self._seedCreationForm
            )

    def post(self):

        # Create the GameSeed.
        gs = GameSeed(
            originator = getDendriteNode(self.request.get('uid')),
            name = self.request.get('name'),
            URL = self.request.get('URL'),
            )
        gs.put()

        # Send back a simple acknowledgement page with the creation form.
        w = self.response.out.write
        w('<html><body>You created: %(fragment)s\n'
          'Use this link to send it to friends and contacts: '

          '<a href=/createcard/%(URL)s>'
          'http://1.latest.xerblin.appspot.com/createcard/%(URL)s'
          '</a>'

          '<hr>'

          'Or create another GameSeed:<br>' % dict(
              URL=str(gs.key()),
              fragment=gameSeedFragment(gs),
              )
          )
        w(self._seedCreationForm)
        w('</body></html>')


class CardHandler(webapp.RequestHandler):
    '''
    Handles creation of Cards for GameSeeds

    GET takes a GameSeed key and returns a form for creating a card.
    POST handles that form.
    '''

    def get(self, gameseed):

        # Check that this key exists.
        gs = dbGet(gameseed)
        if not gs:
            self.error(404)
            return

        # Send a form for creating a card.
        self.response.out.write('''
  <html>
    <body>
      %s
      Send this GameSeed.
      <form action="/createcard/%s" method="post">
        Your uid:<input type="text" name="sender"><br>
        Send to uid:<input type="text" name="recipient"><br>
        <input type="submit" value="Send card to:">
      </form>
    </body>
  </html>''' % (gameSeedFragment(gs), gameseed))

    def post(self, gameseed):

        # Get the GameSeed.
        gs = dbGet(gameseed)
        if not gs:
            self.error(404)
            return

        # Create the card.
        card = Card(
            gameseed = gs,
            sender = getDendriteNode(self.request.get('sender')),
            recipient = getDendriteNode(self.request.get('recipient')),
            )
        card.put()

        # Send a simple acknowledgement page.
        w = self.response.out.write
        w('<html><body>You created:')
        w(cardFragment(card))
        w('</body></html>')


class GameSeedListerHandler(webapp.RequestHandler):

    def get(self, gameseed=None):
        if not gameseed:
            self.listGameSeeds()
            return

        gs = dbGet(gameseed)
        if not gs:
            self.error(404)
            return

        self.response.out.write(
            '<html><body>%s</body></html>' % gameSeedFragment(gs, True)
            )

    def listGameSeeds(self):
        gameseeds = GameSeed.all().order('-creation_time').fetch(20)
        w = self.response.out.write
        w('<html><body>')
        for gs in gameseeds:
            w(gameSeedOneLiner(gs))
        w('</body></html>')


class CardListerHandler(webapp.RequestHandler):

    def get(self, card=None):
        if not card:
            self.listCards()
            return

        card = dbGet(card)
        if not card:
            self.error(404)
            return

        self.response.out.write(
            '<html><body>%s</body></html>' % cardFragment(card)
            )

    def listCards(self):
        w = self.response.out.write
        w('<html><body>')

        recipient = self.request.get('iam')
        if recipient:
            recipient = getDendriteNode(recipient)
            w(repr(recipient))

        q = Card.all().filter('seen =', False)
        if recipient:
            q = q.filter('recipient =', recipient)
        q = q.order('-creation_time')

        cards = q.fetch(20)
        for card in cards:
            w(cardOneLiner(card))
        w('</body></html>')


application = webapp.WSGIApplication(
    [
        ('/', GameSeedHandler),
        ('/creategameseed', GameSeedHandler),
        ('/createcard/(.*)', CardHandler),
        ('/gameseed/(.*)', GameSeedListerHandler),
        ('/gameseeds?', GameSeedListerHandler),
        ('/card/(.*)', CardListerHandler),
        ('/cards?', CardListerHandler),
        ],
    debug=True,
    )


def main():
    run_wsgi_app(application)


if __name__ == '__main__':
    main()



##class MainPage(webapp.RequestHandler):
##
##    def get(self):
##
##        user = users.get_current_user()
##
##        if user:
##            self.response.headers['Content-Type'] = 'text/plain'
##            self.response.out.write('Hello, %s!' %  user.nickname())
##        else:
##            self.redirect(users.create_login_url(self.request.uri))


