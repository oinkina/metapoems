import os
from BeautifulSoup import BeautifulSoup as BSHTML

# indir = '/Users/cssi2014/Desktop/bookRDF'
# for root, dirs, filenames in os.walk(indir):
#     for f in filenames:
#         print f


BS = BSHTML('/Users/cssi2014/Desktop/bookRDF/pg13.rdf')
print BS.pgterms.contents[0].strip()
# root = tree.getroot()

# p = tree.find("pgterms:name")
# print p

# for atype in ET.findall('pgterms:name'):
#   print(atype.get('foobar'))





# >>> p = tree.find("body/p")     # Finds first occurrence of tag p in body
# >>> p
# <Element p at 8416e0c>
# >>> p.text
# "Some text in the Paragraph"
# >>> links = p.getiterator("a")  # Returns list of all links
# >>> links
# [<Element a at b7d4f9ec>, <Element a at b7d4fb0c>]
# >>> for i in links:             # Iterates through all found links
# ...     i.attrib["target"] = "blank"
# >>> tree.write("output.xhtml")