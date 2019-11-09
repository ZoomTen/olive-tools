import sys
import os
import shutil
import uuid
import zlib
import zipfile
from glob import glob
from argparse import ArgumentParser
from lxml import etree, objectify

def phase(title):
    print("\n" + "*"*5, title, "*"*5)
    
def log(string, level="note"):
    print(level+":", string)

def main_func(filename, tempname, outputfile):
    with open(filename,"rb") as prj:
        project_string = prj.read()
        project = objectify.fromstring(project_string)
    
    # create temp directory
    temp_dir = tempname
    root = os.path.join(temp_dir, os.path.splitext(os.path.basename(filename))[0])
    media_folder = os.path.join(root, "media")
    
    try:
        os.mkdir(temp_dir)
        os.mkdir(root)
        os.mkdir(media_folder)
    except:
        log("Can't make temporary folder!", level="error")
        raise
    
    log("Work folder: " + root)
    
    phase("Copy Files")
    # change every media url to its absolute urls
    for media in project.media.getchildren():
        media_origin = os.path.abspath((media.get("url")))
        media_name = os.path.basename((media.get("url")))
        media_url = os.path.join("media", media_name)
        
        media.set("url", media_url)
        try:
            shutil.copy(media_origin, media_folder)
            log("Copying " + media_name)
        except FileNotFoundError:
            log("Can't find file " + media_origin + ". Continuing anyway.", level="warning")
    
    # make modified xml file
    final_project_file = etree.tostring(project, pretty_print=True)
    with open(os.path.join(root, "project.ove"), "wb") as of:
        of.write(final_project_file)
        log("Written project file.")
    
    phase("Compress Project")
    # zip up project file
    with zipfile.ZipFile(outputfile, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as compressed_file:
        for rr, dd, files in os.walk(root):
            for ff in files:
                compressed_file.write(os.path.join(rr,ff), os.path.relpath(os.path.join(rr,ff), temp_dir))
                log("Compressing " + ff)
    
    phase("Finalizing")
    log("Compressed successfully to " + outputfile + "!")
    
        
if __name__ == "__main__":
    parse = ArgumentParser(
                       description="Packs an Olive OVE project file to a \
                                    self-contained zip file, containing the \
                                    project file itself as well as the included\
                                    media. \
                                    This can be useful if you plan to share \
                                    your project files. ",
                       epilog="WARNING: This is built specifically for the\
                               Olive 0.1.x / Chestnut file format.")
    parse.add_argument('input',
                       type=str,
                       help="OVE project filename")
    parse.add_argument('--output', '-o',
                       type=str,
                       help="Name of output zip file, default is the same as \
                             the input file name.")
    
    args = parse.parse_args()
    
    if args.output is None:
        args.output = os.path.splitext(os.path.basename(args.input))[0]+'.zip'
    
    tempname = '.'+uuid.uuid4().hex
    main_func(args.input, tempname, args.output)
    shutil.rmtree(tempname)
    log("Deleted temporary folder.")
        
