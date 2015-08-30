# -*- coding: utf-8 -*-
"""!insult will return a sorry-ass random insult."""
import random
import re

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!insult", text)
    if not match:
        return
    else:
        fh = open('insults.txt')
        lines = fh.readlines()
        fh.close()
        
        this_insult = random.choice(lines)
        
        return this_insult
