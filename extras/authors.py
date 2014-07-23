import os
import webapp2
from google.appengine.ext import ndb


indir = '/Users/cssi2014/Desktop/bookRDF'
authors = []

# for subdir, dirs, files in os.walk(indir):
for f in os.listdir(indir):
	meta = open(f,'r')
	for line in meta:
		if "<pgterms:name>" in line:
			start_tag="<pgterms:name>"
			end_tag="</pgterms:name>"
			authors.append(str(line.split(start_tag)[1].split(end_tag)[0]))



