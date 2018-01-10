import hexchat
import hashlib
import re

__module_name__ = "hash_nick_colors"
__module_version__ = "0.3.0"
__module_description__ = "Consistent nick colors based on simple hash function"

# default nick color list
colors = [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
# load override from prefs
colors_str = hexchat.get_pluginpref("hash_nick_colors.colors")
if colors_str != None:
    colors = [int(c) for c in re.findall("(\d+)", colors_str)]

# default nick->color map
cache = {}
# load override from prefs
override = hexchat.get_pluginpref("hash_nick_colors.override")
for pair in re.findall("\'(\w+)\': (\d+)", override):
    cache[pair[0]] = pair[1]


def hash_color(w):
    color = colors[int(hashlib.md5(w.encode("utf-8")).hexdigest(), 16) % len(colors)]
    cache[w] = color
    return color

def process_message(word, word_eol, userdata):
    if "\003" in word[0]:  # if already colored do not touch; closes event loop
        return hexchat.EAT_NONE

    color = cache[word[0]] if word[0] in cache else hash_color(word[0])
    word[0] = "\003" + str(color) + word[0] + "\003"
    if(len(word) == 3):
        word[2] = "\003" + str(color) + word[2] + "\003"

    hexchat.emit_print(userdata["event"], *word)

    # manually set tab color
    if(userdata["event"] in ["Channel Msg Hilight", "Private Message to Dialog"]):
        hexchat.command("gui color 3")
    else:
        hexchat.command("gui color 2")

    return hexchat.EAT_ALL

def unload(userdata):
    print("Unloading " + __module_name__ + " v" + __module_version__)

events = ["Your Message", "Channel Message", "Channel Msg Hilight", "Private Message to Dialog"]
for event in events:
    hexchat.hook_print(event, process_message, userdata={"event": event})

hexchat.hook_unload(unload)

print("Loaded " + __module_name__ + " v" + __module_version__)
