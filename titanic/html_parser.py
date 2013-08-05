'''
Created on Jul 18, 2013

@author: work
'''
from HTMLParser import HTMLParser
#from html.parser import HTMLParser
import urllib

class LinksParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = 0
        self.data = []
    
    def handle_starttag(self, tag, attributes):
        if tag != 'strong' or tag == 'p' or tag=='a':
            return
        if self.recording:
            self.recording += 1
            return
        for name, value in attributes:
            if name == 'href' or name == 'name':
                return #break
        #else:
        #    return
        self.recording = 1
    
    def handle_endtag(self, tag):
        if tag == 'br' and self.recording:
            self.recording -= 1
    
    def handle_data(self, data):
        if self.recording:
            self.data.append(data)


p = LinksParser()
f = urllib.urlopen("http://www.lva.virginia.gov/exhibits/titanic/p2.htm")
html = f.read()
p.feed(html)
p.close()

print p.data

