import os
import re
import traceback

import DeDRM_tools.DeDRM_plugin.ineptepub as ineptepub
import DeDRM_tools.DeDRM_plugin.ignobleepub as ignobleepub
import DeDRM_tools.DeDRM_plugin.epubtest as epubtest
import DeDRM_tools.DeDRM_plugin.zipfix as zipfix

def decryptepub(infile, outdir, rscpath):
    errlog = ''

    # first fix the epub to make sure we do not get errors
    name, ext = os.path.splitext(os.path.basename(infile))
    bpath = os.path.dirname(infile)
    zippath = os.path.join(bpath,name + '_temp.zip')
    rv = zipfix.repairBook(infile, zippath)
    if rv != 0:
        print("Error while trying to fix epub")
        return rv

    # determine a good name for the output file
    outfile = os.path.join(outdir, name + '_nodrm.epub')

    rv = 1
    # first try with the Adobe adept epub
    if  ineptepub.adeptBook(zippath):
        # try with any keyfiles (*.der) in the rscpath
        files = os.listdir(rscpath)
        filefilter = re.compile("\.der$", re.IGNORECASE)
        files = filter(filefilter.search, files)
        if files:
            for filename in files:
                keypath = os.path.join(rscpath, filename)
                userkey = open(keypath,'rb').read()
                try:
                    rv = ineptepub.decryptBook(userkey, zippath, outfile)
                    if rv == 0:
                        print("Decrypted Adobe ePub with key file {0}".format(filename))
                        break
                except Exception as e:
                    errlog += traceback.format_exc()
                    errlog += str(e)
                    rv = 1
    # now try with ignoble epub
    elif  ignobleepub.ignobleBook(zippath):
        # try with any keyfiles (*.b64) in the rscpath
        files = os.listdir(rscpath)
        filefilter = re.compile("\.b64$", re.IGNORECASE)
        files = filter(filefilter.search, files)
        if files:
            for filename in files:
                keypath = os.path.join(rscpath, filename)
                userkey = open(keypath,'r').read()
                #print userkey
                try:
                    rv = ignobleepub.decryptBook(userkey, zippath, outfile)
                    if rv == 0:
                        print("Decrypted B&N ePub with key file {0}".format(filename))
                        break
                except Exception as e:
                    errlog += traceback.format_exc()
                    errlog += str(e)
                    rv = 1
    else:
        encryption = epubtest.encryption(zippath)
        if encryption == "Unencrypted":
            print("{0} is not DRMed.".format(name))
            rv = 0
        else:
            print("{0} has an unknown encryption.".format(name))

    os.remove(zippath)
    if rv != 0:
        print(errlog)
    return rv
