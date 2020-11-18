import os
import re
from markdown2 import markdown

def process_md(context):
    context = markdown(context, extras=["break-on-newline"])
    context = re.sub(r"!\[\[(.+)\]\]", r"<img src='/medya/\1'>", context)

    return context