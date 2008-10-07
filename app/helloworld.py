from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import users
from models import (
    GameSeed,
    Card,
    gameSeedFragment,
    gameSeedOneLiner,
    cardFragment,
    cardOneLiner,
    )


dbGet = lambda key: db.get(db.Key(key))


class GameSeedHandler(webapp.RequestHandler):

    _seedCreationForm = '''
  <form action="/creategameseed" method="post">
    Your email:<input type="text" name="email"><br>
    GameSeed Name:<input type="text" name="name"><br>
    GameSeed URL:<input type="text" name="URL" size=128><br>
    <input type="submit" value="Create new GameSeed">
  </form>
'''

    def get(self):
        self.response.out.write("""
<html>
<body>%s</body>
</html>""" % self._seedCreationForm)

    def post(self):
        gs = GameSeed(
            originator = users.User(self.request.get('email')),
            name = self.request.get('name'),
            URL = self.request.get('URL'),
            )
        gs.put()
        w = self.response.out.write
        w('<html><body>You created: %s' % gameSeedFragment(gs))
        w('''Use this link to send it to friends and contacts:
<a href=/createcard/%(URL)s>http://1.latest.xerblin.appspot.com/createcard/%(URL)s</a><hr>
Or create another GameSeed:<br>
''' % {'URL': str(gs.key())}
                                )
        w(self._seedCreationForm)
        w('</body></html>')


class CardHandler(webapp.RequestHandler):

    def get(self, gameseed):
        gs = dbGet(gameseed)
        if not gs:
            self.error(404)
            return

        self.response.out.write("""
  <html>
    <body>
      %s
      Send this GameSeed.
      <form action="/createcard/%s" method="post">
        Your email address:<input type="text" name="sender"><br>
        Send to email:<input type="text" name="recipient"><br>
        <input type="submit" value="Send card to:">
      </form>
    </body>
  </html>""" % (gameSeedFragment(gs), gameseed))

    def post(self, gameseed):
        gs = dbGet(gameseed)
        if not gs:
            self.error(404)
            return

        card = Card(
            gameseed = gs,
            sender = users.User(self.request.get('sender')),
            recipient = users.User(self.request.get('recipient')),
            )
        card.put()

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
            """<html><body>%s</body></html>""" % gameSeedFragment(gs, True)
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
            "<html><body>%s</body></html>" % cardFragment(card)
            )

    def listCards(self):
        w = self.response.out.write
        w('<html><body>')
        recipient = self.request.get("iam")
        w(repr(recipient))
        if recipient:
            recipient = users.User(recipient)
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


if __name__ == "__main__":
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


