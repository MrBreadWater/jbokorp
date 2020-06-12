
import sb.util as util
import os
import re
import subprocess

import is_lojban

from bs4 import BeautifulSoup, UnicodeDammit
from unidecode import unidecode
from xml.sax.saxutils import escape, quoteattr

# These are already in the ralju corpora
ignore = ["lo nu binxo.html",
          "la snime blabi.html",
         ]

silly_tags = re.compile(r"^(em|strong|i|a|br)$")

def process(fname, force=False):
    """
    Get the lojban of the html page in fname that comes from the Lojban Tiki.

    Some markup is removed, like <em>, <strong>

    The output is stored in xml in filename resembling the input name.
    """

    pre_name = unidecode(os.path.split(os.path.splitext(fname)[0])[1])
    xml_file = "".join([c for c in pre_name if c.isalpha() or c.isdigit()]).rstrip() + ".xml"

    if os.path.exists(xml_file) and not force:
        return

    soup = BeautifulSoup(open(fname,"r").read())

    if soup is not None:
        
        # remove some silly tags
        for tag in soup.find_all(silly_tags):
            tag.unwrap()
            tag.parent = tag.unwrap

        title = soup.title.string or ""

#        print unidecode(fname), unidecode(title), xml_file
            
        out = ['<text',
            ' title=%s ' % quoteattr(title),
            ' filename=%s ' % quoteattr(fname),
            '>']
        for s in list(soup.strings or []):
            if is_lojban(s):
                out.append('<chunk>')
                out.append(escape(UnicodeDammit(s).unicode_markup))
                out.append('</chunk>')
        out.append('</text>')

        with open(xml_file,"w") as x:
            for o in out:
                try:
                    x.write(o)
                    x.write("\n")
                except UnicodeEncodeError:
                    print("Unicode error in", unidecode(fname))
                    x.write(unidecode(o))

        print("Wrote", xml_file)

def tiki(force = False):
    """Tikify all html pages in the current directory"""
    for d,_,fs in os.walk("."):
        for f in fs:
            if f not in ignore and ".html" in f:
                if d[2:] == "":
                    fname = f
                else:
                    fname = d[2:] + "/" + f
                process(fname,force)

if __name__ == '__main__':
    util.run.main(tiki,process = process,is_lojban = is_lojban)

