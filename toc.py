'''
toc
===================================

This plugin generates tocs for pages and articles.
'''

from pelican import signals, contents
from bs4 import BeautifulSoup
import re

class HtmlTreeNode:
    def __init__(self, parent, header):
        self.childs = []
        self.parent = parent
        self.header = header
    
    def add(self, new_header):
        if (self.header==None):
            return HtmlTreeNode(None, new_header)
        
        if (new_header.name > self.header.name):
            #can insert as child
            new_node = HtmlTreeNode(self,new_header)
            self.childs = self.childs ++ [new_node]
            return new_node
        elif (new_header.name <= self.header.name):
            if(self.parent!=None):
                return self.parent.add(new_header)
            else:
                #cant go up higher, make new parent
                new_parent = HtmlTreeNode(None,new_header)
                new_parent.add(self)
                return new_parent


def generate_toc(instance):
    if instance._content is not None:
        toc = {}
        node = HtmlTreeNode(None, None)
        
        content = instance._content
        soup = BeautifulSoup(content)
        for header in soup.findAll(re.compile("^h\d")):
            node = node.add(header)
            #add to toclist
            #set unique id if needed
        print(repr(node))
        input()
        instance.toc = toc


def register():
    signals.content_object_init.connect(generate_toc)
