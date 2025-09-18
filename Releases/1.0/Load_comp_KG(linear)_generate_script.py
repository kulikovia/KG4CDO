import xml.etree.ElementTree as xml
import random
from random import randrange
from datetime import datetime
from datetime import timedelta

Max_Objects = 7500000   #Model 1
Max_Options = 7500000   #Model 2
Max_Step_1 = 100000 #Maximum number of model elements in each rdf file
Max_Step_2 = 50000  #Maximum number of model elements in each rdf file

#Constants
SPARQL_path = "C:/Blazegraph/1" #The path is used for UPDATE RDF DB creation script
Model_path = "Linear_model/"    #The path for output files


def createXML(filename):

#Open SPARQL file
    spql = open(Model_path + "sparql_script.spql", "wt")

# Add header
    header = str("<?xml version='1.0' encoding='UTF-8'?>\n<rdf:RDF\nxmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'\nxmlns:vCard='http://www.w3.org/2001/vcard-rdf/3.0#'\nxmlns:my='http://127.0.0.1/bg/ont/test1#'\n>")

    f = open(Model_path + filename + "_static.nq", "wt")
    f.write(header)

# Model 1 hierarchy definition
# Add Core definitions
    f.write("\n<!--Model 1 Core definitions-->\n<rdf:Description rdf:about='http://127.0.0.1/Core_1/'>\n<my:has_id>Core_1</my:has_id>\n</rdf:Description>")

# Model 2 hierarchy definition
# Add Core definitions
    f.write("\n<!--Model 2 Core definitions-->\n<rdf:Description rdf:about='http://127.0.0.1/Core_2/'>\n<my:has_id>Core_2</my:has_id>\n</rdf:Description>")
    f.write("\n</rdf:RDF>\n")
    f.close()
    spql.write("\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_static.nq>;\n")

# Add Object  definitions
    FileNum = 0
    i = 1
    k = 1
    while i <= Max_Objects:
        FileNum = FileNum + 1
        f = open(Model_path + filename + "_object_" + str(FileNum) + "_.nq", "at")
        f.write(header)
        f.write("\n<!--Objects definitions-->\n")
        while k <= Max_Step_1:
            body = str("<rdf:Description rdf:about='http://127.0.0.1/Object_") + str(i) + str("/'>\n<my:has_id>Object_") + str(i) + str("</my:has_id>\n<my:has_parent_id>Core_1</my:has_parent_id>\n</rdf:Description>\n")
            f.write(body)
            i = i + 1
            k = k + 1
        f.write("\n</rdf:RDF>\n")
        f.close()
        spql.write("\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_object_" + str(FileNum) + "_.nq>;\n")
        k = 1

# Add Options  definitions
    FileNum = 0
    i = 1
    k = 1
    while i <= Max_Options:
        FileNum = FileNum + 1
        f = open(Model_path + filename + "_option_" + str(FileNum) + "_.nq", "at")
        f.write(header)
        f.write("\n<!--Options definitions-->\n")
        while k <= Max_Step_1:
            body = str("<rdf:Description rdf:about='http://127.0.0.1/Option_") + str(i) + str(
                "/'>\n<my:has_id>Option_") + str(i) + str("</my:has_id>\n<my:has_parent_id>Core_2</my:has_parent_id>\n</rdf:Description>\n")
            f.write(body)
            i = i + 1
            k = k + 1
            if i >= Max_Options: break
        f.write("\n</rdf:RDF>\n")
        f.close()
        spql.write("\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_option_" + str(FileNum) + "_.nq>;\n")
        k = 1

 # Add Object-option links links Type-1  definitions
    FileNum = 0
    i = 1
    k = 1
    while i <= Max_Objects:
        FileNum = FileNum + 1
        f = open(Model_path + filename + "_links_1_" + str(FileNum) + "_.nq", "at")
        f.write(header)
        f.write("\n<!--Add Object-option links Type-Linear-->\n")
        while k <= Max_Step_1:
            body = str("<rdf:Description rdf:about='http://127.0.0.1/Object_") + str(i) + str(
                "/'>\n<my:has_option_id>Option_") + str(random.randint(1, Max_Options)) + str("</my:has_option_id>\n</rdf:Description>\n")
            f.write(body)
            i = i + 1
            k = k + 1
        f.write("\n</rdf:RDF>\n")
        f.close()
        spql.write("\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_links_1_" + str(FileNum) + "_.nq>;\n")
        k = 1


    spql.close()

if __name__ == "__main__":
    createXML("KG_telecom")
