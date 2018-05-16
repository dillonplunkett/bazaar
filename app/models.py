from datetime import datetime
import random
import json
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

with open("cube.json", "r") as cube_file:
    cube_cards = json.load(cube_file)

permitted_bidders = db.Table(
    "permitted_bidders",
    db.Column("auction_id", db.Integer, db.ForeignKey("auction.id"),
              primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"),
              primary_key=True)
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    balances = db.relationship("Balance", backref="holder", lazy="dynamic")
    bids = db.relationship("Bid", backref="bidder", lazy="dynamic")
    lots = db.relationship("Lot", backref="winner", lazy="dynamic")
    created_auctions = db.relationship("Auction", backref="creator",
                                       lazy="dynamic")

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_funds(self, auction):
        return self.balances.filter_by(auction=auction).first().amount > 0


class Pool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cards = db.Column(db.PickleType)
    auctions = db.relationship("Auction", backref="pool", lazy="dynamic")

    def __repr__(self):
        return f"<Pool {self.id} for Auction {self.auctions.first()}>"

    def get_random(self, size):
        return random.sample(self.cards, size)

    def remove_from_pool(self, drafted):
        copy = self.cards[:]
        for card in drafted:
            copy.remove(card)
        self.cards = copy

    def new_from_cube(self):
        self.cards = list(cube_cards.keys())


class Auction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    starting_balance = db.Column(db.Integer)
    time_limit = db.Column(db.Integer, nullable=True)
    default_lot = db.Column(db.Integer, nullable=True)
    balances = db.relationship("Balance", backref="auction", lazy="dynamic")
    lots = db.relationship("Lot", backref="auction", lazy="dynamic")
    users = db.relationship("User", secondary=permitted_bidders,
                            backref=db.backref("auctions", lazy="dynamic"),
                            lazy="dynamic")
    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    pool_id = db.Column(db.Integer, db.ForeignKey("pool.id"))

    def __repr__(self):
        return f"<Auction {self.id}>"

    def add_lot(self, size=None, card=None, active=True):
        if size:
            lot = Lot(auction=self, content=self.pool.get_random(size),
                      active=active)
        elif card:
            lot = Lot(auction=self, content=[card], active=active)
        else:
            lot = Lot(auction=self, active=active)
        db.session.add(lot)

    def current_lot(self):
        return self.lots.filter_by(active=True).first()

    def is_complete(self):
        return not any([user.has_funds(self) for user in self.users])


class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    auction_id = db.Column(db.Integer, db.ForeignKey("auction.id"))
    amount = db.Column(db.Integer)

    def __repr__(self):
        return f"<Balance for {self.user_id} in {self.auction_id}>"


class Lot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    active = db.Column(db.Boolean)
    auction_id = db.Column(db.Integer, db.ForeignKey("auction.id"))
    winner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    bids = db.relationship("Bid", backref="lot", lazy="dynamic")
    content = db.Column(db.PickleType, nullable=True)

    def __repr__(self):
        return f"<Lot {self.id}>"

    def final_bid(self, user):
        user_bids = self.bids.filter_by(bidder=user)
        return user_bids.order_by(Bid.timestamp.desc()).first()

    def final_bids(self):
        final_bids = [self.final_bid(user) for user in self.auction.users
                      if self.final_bid(user)]
        final_bids.sort(key=lambda bid: bid.timestamp) # seconday sort
        final_bids.sort(key=lambda bid: bid.amount, reverse=True) # primary sort
        return final_bids

    def max_bid(self):
        final_bids = self.final_bids()
        if final_bids:
            return final_bids[0]
        else:
            return None

    def waiting_on(self):
        return [user for user in self.auction.users
                if not self.final_bid(user) and user.has_funds(self.auction)]

    def record_winner(self):
        winning_bid = self.max_bid()
        self.winner = winning_bid.bidder
        winner_balance = self.winner.balances.filter_by(auction=self.auction).first()
        winner_balance.amount = winner_balance.amount - winning_bid.amount
        self.active = False

    def reset(self):
        for bid in self.bids:
            db.session.delete(bid)
        self.timestamp = datetime.utcnow()


class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    lot_id = db.Column(db.Integer, db.ForeignKey("lot.id"))
    amount = db.Column(db.Integer)

    def __repr__(self):
        return f"<Bid {self.id}>"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
