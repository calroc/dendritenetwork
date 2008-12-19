from random import choice
from models import (
    DendriteNode,
    GameSeed,
    Card,
    )


D = [DendriteNode(uid=n) for n in range(123)]
for d in D: d.put()


G = [
    GameSeed(
        originator = choice(D),
        name = 'gs%i' % n,
        URL = 'http://www.%i.org/' % n,
        )
    for n in range(20)
    ]
for gs in G: gs.put()

C = []
for gs in G:
    pool = D[:]
    pool.pop(pool.index(gs.originator))
    card = Card(
        gameseed=gs,
        sender=gs.originator,
        recipient=choice(pool),
        )
    card.put()
    del pool
    C.append(card)

