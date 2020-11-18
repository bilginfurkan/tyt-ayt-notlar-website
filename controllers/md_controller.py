import os
import re


def process_md(context):
    context = re.sub(r"!\[\[(.+)\]\]", r"<img src='/medya/\1'>", context)
    return context