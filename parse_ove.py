from lxml import etree

class OVE:
    version = ""
    url     = ""
    folders = []
    media   = []
    sequences=[]
    
    def __init__(self):
        pass
    
    def parsefile(self, filename):
        project_string = open(filename,"rb").read()
        project = etree.fromstring(project_string)
        
        for node in project.getchildren():
            if node.tag == "version":
                self.version = node.text
            elif node.tag == "url":
                self.url = node.text
            elif node.tag == "folders":
                for folder in node.getchildren():
                    self.folders.append(folder)
            elif node.tag == "media":
                for media in node.getchildren():
                    self.media.append(media)
            elif node.tag == "sequences":
                for sequence in node.getchildren():
                    self.sequences.append(sequence)
            else:
                pass

                
if __name__ == "__main__":
    Project = OVE()
    
    Project.parsefile("test.ove") # fixed file for now
    print("Project url:\n", Project.url)
    print("Spec version:\n", Project.version)
    print("Project bin folders:\n", Project.folders)
    print("Project bin media:\n", Project.media)
    print("Project bin sequences:\n", Project.sequences)
    
    print("\n"+"="*20+"FOLDERS"+"="*20)
    for folder in Project.folders:
        print(folder.attrib["name"])
    
    print("\n"+"="*20+"MEDIA"+"="*20)
    for media in Project.media:
        print(media.attrib["name"])
    
    print("\n"+"="*20+"SEQUENCE"+"="*20)
    for sequence in Project.sequences:
        print(sequence.attrib["name"])
