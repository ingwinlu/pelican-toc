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
        if(self.header==None or self.header.name < new_header.name):
            #can add as child
            new_node = HtmlTreeNode(self, new_header)
            self.childs = self.childs + [new_node]
            return new_node
        elif(self.header.name == new_header.name):
            #new sibling
            new_node = HtmlTreeNode(self.parent, new_header)
            self.parent.childs = self.parent.childs + [new_node]
            return new_node
        elif(self.header.name > new_header.name):
            #new parent
            if(self.parent == None):
                new_node = HtmlTreeNode(None, new_header)
                self.parent = new_node
                new_node.childs = [self]
                return new_node
            else:
                return self.parent.add(new_header)
    
    def __repr__(self):
        ret = repr(self.header) + " Childs:" + repr(self.childs)
        return ret

def generate_toc(content):
    if isinstance(content, contents.Static):
        return
    
    toc = []
    #tree = node = HtmlTreeNode(None, None)
    
    soup = BeautifulSoup(content._content)
    for header in soup.findAll(re.compile("^h\d")):
        toc = toc + [header.prettify(formatter="html")]
        #node = node.add(header)
        #add to toclist
        #set unique id if needed
    #content._content = soup.decode()
    content.toc = toc


def register():
    signals.content_object_init.connect(generate_toc)
