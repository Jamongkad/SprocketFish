import re, os, sys
from mako.template import Template
from mako.lookup import TemplateLookup

def gather_view_files():

    directories = ['./views']

    [directories.append(dirpath) for dirpath, dirnames, filenames in os.walk(os.path.abspath('./modules'))
        if re.search('(?<=views)', dirpath)]

    mylookup = TemplateLookup(directories, output_encoding='utf-8')

    return mylookup

def render(templatename, **kwa):
    mytemplate = gather_view_files().get_template(templatename)
    return mytemplate.render(**kwa)
