<!-- omit in TOC -->
# Bazaar

<!-- omit in TOC -->
## Table of Contents
- [About](#about)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Launching Bazaar](#launching-bazaar)
  - [Running a Draft](#running-a-draft)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## About
_Bazaar_ lets you run online auction drafts (as in fantasy sports). It is primarily designed for drafting Magic: the Gathering cubes, but can be adapted for any kind of auction draft.

## Getting Started

### Prerequisites
- Python 3.6+
### Installation
1. Navigate to the project directory. Then run the following commands to create a virtual environment with the necessary packages.
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
2. Replace `cube_list.txt` with your cube list (one card per line).
3. Build a folder of card images by running `python fetch_images.py`. This will take about one minute per 100 cards. 
4. Initialize the database with `flask db upgrade`.
5. _Bazaar_ supports custom cards. However, `cube_list.txt` must only contain real card names. To implement custom cards, ensure there is a unique "placeholder" card name in `cube_list.txt` for each custom card. Then, create a file called `custom_cards.txt` with a list of `placeholder_cardname -> custom_cardname`, one per line. Then, place images for your custom cards in the `app/static/card_images` directory. The image names must be the custom card names with all non-alphanumeric characters removed and must end in `.jpg` (e.g., `CustomCardname7.jpg`).
## Usage
### Launching Bazaar
1. Run `python bazaar.py`.
2. By default, you can access _Bazaar_ on port 5000. If you are running _Bazaar_ on your computer and not a publically accessible server, you can use [ngrok][ngrok] to allow drafters to connect. It creates a web address for a given port on your computer and there are easy-to-follow instructions on its website.
### Running a Draft
1. After creating an account, any user can create a draft from the `New Draft` page. They become the owner of that draft. There are a number of configurable options:  
   - `Starting Balance` sets the amount of currency that each drafter begins with.
   - `Default Lot Size` controls how many cards appear in each lot. During a draft, the owner of that draft may nominate a particular card to be the next lot. This can be done for the first lot with `First Nomination`.
   - `Time Limit` is currently unenforced except that the clock changes color when it has passed. The owner of the auction can manually close bidding to enforce the limit (or at any time).
2. After each player has placed a bid, the bids and winner are displayed and the lot is added to the winner's pool. The owner of the draft must click a button to advance to the next lot (to allow drafters time to see the outcome).
3. Each player's currency balance is visible to everyone else on the draft page. Each player's pool of cards that they have won is visible at all times on pages linked from the draft page.
4. The draft is complete when no player has any currency left, the pool of cards has been exhausted, or (most commonly) by stopping after a pre-designated number of lots.
### Notes
- If two players bid the same amount, the player who submitted their bid first wins the lot. 
- Players who have already bid on a lot can submit another bid to change their bid. The most recent bid from each player is used. (Bidding closes when every player has submitted a bid or if the auction owner closes it manually before then.)

## Contributing
Contributions are warmly welcomed. Report bugs using the [issue tracker][issues]. To contribute code, submit a [pull request][pull_requests].

## License
Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## Acknowledgments
Miguel Grinberg's [Flask Mega-Tutorial][mega_tutorial] was instrumental in the creation of _Bazaar_.

_Bazaar_ uses the wonderful [Scryfall](https://scryfall.com/) API.


[issues]: https://github.com/dillonplunkett/bazaar/issues
[pull_requests]: https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests
[mega_tutorial]: https://courses.miguelgrinberg.com/p/flask-mega-tutorial
[ngrok]: https://ngrok.com
