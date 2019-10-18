# -*- coding: utf-8 -*-
import hashlib

# start with a simple exercise: read message from input, encode in utf8, compute hash, print it

NB_CHAR_MATCHED = 3

# TODO: define a md5 function to generate the hash of a string. The str must be converted to a byte array
def md5(str):
    return ""


msg = "F*ck you, professor!"

msg_hash = md5(msg)

print(msg_hash)

while True:
    # TODO: generate a (meaningful) message
    new_msg = ""

    print(new_msg)

    # TODO: stop if the hash of the generated message matches the hash of the original message for the first
    #  NB_CHAR_MATCHED characters
    if True:
        break

print("The hash of message '%s' matches the first %d digits (%.1f bytes) of the hash of the original message" % (new_msg, NB_CHAR_MATCHED, NB_CHAR_MATCHED / 2))
print()
print("H_original = %s" % msg_hash)
print("H_new = %s" % md5(new_msg))
