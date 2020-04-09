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
_Bazaar_ hosts online auction drafts (as in fantasy sports). It is primarily designed for drafting Magic: the Gathering cubes, but can be adapted for any kind of auction draft.

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
3. If you use any custom cards, replace `custom_cards.txt` with a file of `replaced_cardname -> custom_cardname` (one per line). Otherwise, delete `custom_cards.txt`.
4. Build a folder of card images by running `python fetch_images.py`

## Usage
### Launching Bazaar
TODO: Setup
### Running a Draft
1. After creating an account, any user can create a draft from the `New Draft` page. They become the owner of that draft. There are a number of configurable options:  `Starting Balance` sets the amount of token currency that each drafter begins with. The `Default Lot Size` controls how many cards appear in each lot. During a draft, the owner of that draft may nominate a particular card to be the next lot. This can be done for the first lot with `First Nomination`. The `Time Limit` is currently unenforced except that the clock changes color when it has passed. The owner of the auction can manually close bidding to enforce the limit (or at any time).
2. After each player has placed a bid, the bids and winner are displayed and the lot is added to the winner's pool. The owner of the draft must click a button to advance to the next lot (to allow drafters time to see the outcome).
3. Each player's balance of token currency is visible to everyone else on the draft page. Each player's pool of cards that they have won is visible at all times on pages linked from the draft page.
4. The draft is complete when no player has any currency left, the pool of cards has been exhausted, or after a designated number of cards have been picked. Currently the number of cards that have been picked must be tracked manually. This is the next feature to be implemented. 

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
