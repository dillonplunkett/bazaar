from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (BooleanField, HiddenField, IntegerField, PasswordField,
                     SelectMultipleField, StringField, SubmitField)
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import (InputRequired, EqualTo, NumberRange, Optional,
                                ValidationError)
from app.models import Auction, Balance, User, cube_cards


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    remember_me = BooleanField("Remember Me")
    submit_login = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    password2 = PasswordField("Repeat Password", validators=[InputRequired(),
                              EqualTo("password")])
    submit_register = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("That username is taken.")


class CreateForm(FlaskForm):
    usernames = SelectMultipleField("Users:", validators=[InputRequired()],
                                    widget=ListWidget(prefix_label=False),
                                    option_widget=CheckboxInput())
    starting_balance = IntegerField("Starting Balance:",
                                    validators=[InputRequired(),
                                                NumberRange(min=1)])
    default_lot = IntegerField("Default Lot Size:",
                               validators=[Optional(),
                                           NumberRange(min=0, max=15)])
    time_limit = IntegerField("Time Limit (seconds):",
                              validators=[Optional(), NumberRange(min=1)])
    first_nom = StringField("First Nomination:")
    submit_create = SubmitField("Create")

    def validate_first_nom(self, first_nom):
        if self.default_lot.data is not None and not first_nom.data:
            return
        if first_nom.data not in cube_cards.keys():
            raise ValidationError("That card isn't in the pool.")


class BidForm(FlaskForm):
    auction_id = HiddenField()
    lot_id = HiddenField()
    amount = IntegerField("Bid:", validators=[Optional(), NumberRange(min=0)])
    submit_bid = SubmitField("Place Bid")

    def validate_amount(self, amount):
        if not amount.data:
            return
        balance = Balance.query.filter_by(
            holder=current_user, auction_id=self.auction_id.data).first()
        if amount.data > balance.amount:
            raise ValidationError("You don't have that much to bid.")


class CloseBiddingForm(FlaskForm):
    submit_close = SubmitField("Close Bidding")


class AdvanceForm(FlaskForm):
    auction_id = HiddenField()
    next_lot = StringField("Set Lot:", validators=[Optional()])
    submit_advance = SubmitField("Advance")
    submit_reset = SubmitField("Reset")

    def validate_next_lot(self, next_lot):
        if not next_lot.data:
            return
        auction = Auction.query.filter_by(id=self.auction_id.data).first()
        pool = auction.pool
        try:
            num_cards = int(next_lot.data)
            if num_cards < 0 or num_cards > 15:
                raise ValidationError("Lots must be between 0 and 15 cards.")
            cards_in_pool = len(pool.cards)
            if num_cards > cards_in_pool:
                raise ValidationError(f"Only {cards_in_pool} cards left.")
        except ValueError:
            just_sold = auction.current_lot().content
            if just_sold is None:
                just_sold = []
            if next_lot.data not in pool.cards or next_lot.data in just_sold:
                raise ValidationError("That card isn't in the pool.")
