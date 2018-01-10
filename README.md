### hash_nick_colors.py

Hexchat script for consistent nick colors based on simple hash function.

#### Preferences

There are two prefs that can be set in `addon_python.conf`:

* `colors` takes an array of colors to use for nicks:
  * `hash_nick_colors.colors = [22, 23, 24, 25, 26, 27, 28, 29]`
* `override` takes a dict of nick-color pairs that overrides the hash function:
  * `hash_nick_colors.override = {'Alice': 30, 'Bob': 31}`
