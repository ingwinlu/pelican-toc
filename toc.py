'''
toc
===================================

This plugin generates tocs for pages and articles.
'''

from pelican import signals, contents
from bs4 import BeautifulSoup, Comment
import re
import unicodedata

'''
stolen from python.extensions.headerid
https://github.com/waylan/Python-Markdown/blob/master/markdown/extensions/headerid.py
'''
IDCOUNT_RE = re.compile(r'^(.*)_([0-9]+)$')

def slugify(value, separator):
    """ Slugify a string, to make it URL friendly. """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = re.sub('[^\w\s-]', '', value.decode('ascii')).strip().lower()
    return re.sub('[%s\s]+' % separator, separator, value)

def unique(id, ids):
    """ Ensure id is unique in set of ids. Append '_1', '_2'... if not """
    while id in ids or not id:
        m = IDCOUNT_RE.match(id)
        if m:
            id = '%s_%d'% (m.group(1), int(m.group(2))+1)
        else:
            id = '%s_%d'% (id, 1)
    ids.add(id)
    return id
'''
end stolen
'''

class HtmlTreeNode:
    def __init__(self, parent, header, level, id):
        self.childs = []
        self.parent = parent
        self.header = header
        self.level = level
        self.id = id

    def add(self, new_header, ids):
        new_level = new_header.name
        new_string = new_header.string
        new_id = new_header.attrs.get('id')
        if(new_string==None): #not the only child!
            new_string = new_header.find_all(text=lambda t: not isinstance(t, Comment), recursive=True)
            new_string = "".join(new_string)
        if(new_id==None): #no id available, generate one
            new_id=slugify(new_string, '-')
        new_id=unique(new_id,ids) # make sure id is unique
        new_header.attrs['id'] = new_id
        if(self.level < new_level):
            #can add as child
            new_node = HtmlTreeNode(self, new_string, new_level, new_id)
            self.childs = self.childs + [new_node]
            return new_node, new_header
        elif(self.level == new_level):
            #new sibling
            new_node = HtmlTreeNode(self.parent, new_string, new_level, new_id)
            self.parent.childs = self.parent.childs + [new_node]
            return new_node, new_header
        elif(self.level > new_level):
            #let parent handle it
            return self.parent.add(new_header, ids)

    def toString(self):
        ret = ""
        if (self.parent==None):
            ret = ret + "<div id='toc'><ul>"
        ret = ret + "<li><a class='toc-href' href='#{0}' title='{1}'>{1}</a>".format(self.id, self.header)
        if (self.childs != []):
            ret = ret + "<ul>"
        for child in self.childs:
            ret = ret + child.toString()
        if (self.childs != []):
            ret = ret + "</ul>"
        ret = ret + "</li>"
        if (self.parent==None):
            ret = ret + "</ul></div>"
        return ret

def generate_toc(content):
    if isinstance(content, contents.Static):
        return
    all_ids = set()
    tree = node = HtmlTreeNode(None, content.metadata.get('title', 'Title'), "h0", "")
    soup = BeautifulSoup(content._content, 'html.parser')
    settoc = False
    for header in soup.findAll(re.compile("^h\d")):
        settoc = True
        node, new_header = node.add(header, all_ids)
        header.replaceWith(new_header)#to get our ids back into soup
    if (settoc):
        content.toc = BeautifulSoup(tree.toString()).decode(formatter="html")
    content._content = soup.decode(formatter="html")

def register():
    signals.content_object_init.connect(generate_toc)
