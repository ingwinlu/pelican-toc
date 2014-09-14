'''
toc
===================================

This plugin generates tocs for pages and articles.
'''

from pelican import signals
from bs4 import BeautifulSoup
import re

def generate_toc(instance):
    print(repr(instance))
    if instance._content is not None:
        toc = {}
        
        content = instance._content
        soup = BeautifulSoup(content)
        for header in soup.findAll(re.compile("^h\d")):
            print(header)
            #add to toclist
            
            #set unique id if needed
    

def register():
    signals.content_object_init.connect(generate_toc, sender=contents.Article)
    signals.content_object_init.connect(generate_toc, sender=contents.Page)
