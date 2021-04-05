import os, sys
from PIL import Image

def has_ext(name):
    ext_set = {'png', 'jpeg'}
    if name.rpartition('.')[-1] in ext_set:
        return True
    else:
        return False

def resize_img(fpath, basewidth, outname):
    outfile = os.path.dirname(fpath)
    outfile = outfile+'/'+outname
    if not has_ext(outname):
        outfile = outfile+'.'+fpath.rpartition('.')[-1]

    if fpath != outfile:
        try:
            img = Image.open(fpath)
            wpercent = (float(basewidth)/float(img.size[0]))
            hsize = int(img.size[1]*float(wpercent))
            img = img.resize((int(basewidth),hsize), Image.ANTIALIAS)
            img.save(outfile) 
        except IOError:
            print(f"cannot create thumbnail for {fpath}")
