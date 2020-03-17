import os
import time
from urllib.request import urlopen, urlretrieve
from urllib.parse import urlencode

imgs_dir = "app/static/card_images"

with open("cube_list.txt", 'r') as cube_file:
    cube_list = [line.strip().split(" //")[0] for line in cube_file]  # TODO: Do split cards works?

# TODO: Use bulk data from Scryfall to make this faster.

os.makedirs(imgs_dir, exist_ok=True)

for card in cube_list:
    image_file = os.path.join(imgs_dir, f"{card}.jpg".replace(" ", "_"))
    if not os.path.isfile(image_file):
        print(card)
        redir_to_image = f"https://api.scryfall.com/cards/named?fuzzy={card}&format=image&version=normal".replace(" ", "%20") # TODO: 404?
        image_url = urlopen(redir_to_image).geturl()
        urlretrieve(redir_to_image, image_file)
        # Scryfall requests waiting 100ms between requests.
        time.sleep(.1)

# TODO (Eventually): Remove card images that aren't needed anymore.
