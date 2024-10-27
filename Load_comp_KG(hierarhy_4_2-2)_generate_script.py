import xml.etree.ElementTree as xml
import random
from random import randrange
from datetime import datetime
from datetime import timedelta

Max_Level_2 = 244515
Max_Level_3 = 660191
Max_Level_4 = 1782514
Max_Objects_1 = 4812789   #Model 1 lowest level
Max_Objects_2 = 4812789   #Model 2 lowest level
Max_Step_1 = 100000 #Maximum number of model elements in each rdf file
Max_Step_2 = 50000  #Maximum number of model elements in each rdf file

#Constants
SPARQL_path = "C:/Blazegraph/1" #The path is used for UPDATE RDF DB creation script
Model_path = "Hierarchy_model/" #The path for output files


def createXML(filename):

#Open SPARQL file
    spql = open(Model_path + "sparql_script.spql", "wt")

# Add header
    header = str("<?xml version='1.0' encoding='UTF-8'?>\n<rdf:RDF\nxmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'\nxmlns:vCard='http://www.w3.org/2001/vcard-rdf/3.0#'\nxmlns:my='http://127.0.0.1/bg/ont/test1#'\n>")

    f = open(Model_path + filename + "_static.nq", "wt")
    f.write(header)

# Models core definition
    f.write("\n<!--Model 1 Core definitions-->\n<rdf:Description rdf:about='http://127.0.0.1/Core_1/'>\n<my:has_id>Core_1</my:has_id>\n</rdf:Description>")
    f.write("\n<!--Model 2 Core definitions-->\n<rdf:Description rdf:about='http://127.0.0.1/Core_2/'>\n<my:has_id>Core_2</my:has_id>\n</rdf:Description>")
    f.write("\n</rdf:RDF>\n")
    f.close()

# Model 1 hierarchy definition
# Add Level 2 definitions
    FileNum = 0
    i = 1
    k = 1
    while i <= Max_Level_2:
        FileNum = FileNum + 1
        f = open(Model_path + filename + "_Model1_level2_" + str(FileNum) + "_.nq", "at")
        f.write(header)
        f.write("\n<!--Objects definitions-->\n")
        while k <= Max_Step_1:
            body = str("<rdf:Description rdf:about='http://127.0.0.1/Core_1_Level_2_") + str(i) + str(
                "/'>\n<my:has_id>Core_1_Level_2_") + str(i) + str(
                "</my:has_id>\n<my:has_parent_id><rdf:Description rdf:about='http://127.0.0.1/Core_1/' /></my:has_parent_id>\n</rdf:Description>\n")

            f.write(body)
            i = i + 1
            k = k + 1
            if i > Max_Level_2:
                break
        f.write("\n</rdf:RDF>\n")
        f.close()
        spql.write("\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_Model1_level2_" + str(FileNum) + "_.nq>;\n")
        k = 1

# Add Level 3 definitions
    FileNum = 0
    i = 1
    k = 1
    while i <= Max_Level_3:
        FileNum = FileNum + 1
        f = open(Model_path + filename + "_Model1_level3_" + str(FileNum) + "_.nq", "at")
        f.write(header)
        f.write("\n<!--Objects definitions-->\n")
        while k <= Max_Step_1:
            body = str("<rdf:Description rdf:about='http://127.0.0.1/Core_1_Level_3_") + str(i) + str(
                "/'>\n<my:has_id>Core_1_Level_3_") + str(i) + str(
                "</my:has_id>\n<my:has_parent_id><rdf:Description rdf:about='http://127.0.0.1/Core_1_Level_2_") + str(random.randint(1, Max_Level_2)) + str(
                "/' /></my:has_parent_id>\n</rdf:Description>\n")

            f.write(body)
            i = i + 1
            k = k + 1
            if i > Max_Level_3:
                break
        f.write("\n</rdf:RDF>\n")
        f.close()
        spql.write(
            "\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_Model1_level3_" + str(FileNum) + "_.nq>;\n")
        k = 1

# Add Level 4 definitions
    FileNum = 0
    i = 1
    k = 1
    while i <= Max_Level_4:
        FileNum = FileNum + 1
        f = open(Model_path + filename + "_Model1_level4_" + str(FileNum) + "_.nq", "at")
        f.write(header)
        f.write("\n<!--Objects definitions-->\n")
        while k <= Max_Step_1:
            body = str("<rdf:Description rdf:about='http://127.0.0.1/Core_1_Level_4_") + str(i) + str(
                "/'>\n<my:has_id>Core_1_Level_4_") + str(i) + str(
                "</my:has_id>\n<my:has_parent_id><rdf:Description rdf:about='http://127.0.0.1/Core_1_Level_3_") + str(random.randint(1, Max_Level_3)) + str(
                "/' /></my:has_parent_id>\n</rdf:Description>\n")

            f.write(body)
            i = i + 1
            k = k + 1
            if i > Max_Level_4:
                break
        f.write("\n</rdf:RDF>\n")
        f.close()
        spql.write(
            "\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_Model1_level4_" + str(FileNum) + "_.nq>;\n")
        k = 1


# Model 2 hierarchy definition
# Add Level 2 definitions
    FileNum = 0
    i = 1
    k = 1
    while i <= Max_Level_2:
        FileNum = FileNum + 1
        f = open(Model_path + filename + "_Model2_level2_" + str(FileNum) + "_.nq", "at")
        f.write(header)
        f.write("\n<!--Objects definitions-->\n")
        while k <= Max_Step_1:
            body = str("<rdf:Description rdf:about='http://127.0.0.1/Core_2_Level_2_") + str(i) + str(
                "/'>\n<my:has_id>Core_2_Level_2_") + str(i) + str(
                "</my:has_id>\n<my:has_parent_id><rdf:Description rdf:about='http://127.0.0.1/Core_2/' /></my:has_parent_id>\n</rdf:Description>\n")

            f.write(body)
            i = i + 1
            k = k + 1
            if i > Max_Level_2:
                break
        f.write("\n</rdf:RDF>\n")
        f.close()
        spql.write(
            "\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_Model2_level2_" + str(FileNum) + "_.nq>;\n")
        k = 1


# Add Level 3 definitions
    FileNum = 0
    i = 1
    k = 1
    while i <= Max_Level_3:
        FileNum = FileNum + 1
        f = open(Model_path + filename + "_Model2_level3_" + str(FileNum) + "_.nq", "at")
        f.write(header)
        f.write("\n<!--Objects definitions-->\n")
        while k <= Max_Step_1:
            body = str("<rdf:Description rdf:about='http://127.0.0.1/Core_2_Level_3_") + str(i) + str(
                "/'>\n<my:has_id>Core_2_Level_3_") + str(i) + str(
                "</my:has_id>\n<my:has_parent_id><rdf:Description rdf:about='http://127.0.0.1/Core_2_Level_2_") + str(random.randint(1, Max_Level_2)) + str(
                "/' /></my:has_parent_id>\n</rdf:Description>\n")

            f.write(body)
            i = i + 1
            k = k + 1
            if i > Max_Level_3:
                break
        f.write("\n</rdf:RDF>\n")
        f.close()
        spql.write(
            "\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_Model2_level3_" + str(FileNum) + "_.nq>;\n")
        k = 1

# Add Level 4 definitions
    FileNum = 0
    i = 1
    k = 1
    while i <= Max_Level_4:
        FileNum = FileNum + 1
        f = open(Model_path + filename + "_Model2_level4_" + str(FileNum) + "_.nq", "at")
        f.write(header)
        f.write("\n<!--Objects definitions-->\n")
        while k <= Max_Step_1:
            body = str("<rdf:Description rdf:about='http://127.0.0.1/Core_2_Level_4_") + str(i) + str(
                "/'>\n<my:has_id>Core_2_Level_4_") + str(i) + str(
                "</my:has_id>\n<my:has_parent_id><rdf:Description rdf:about='http://127.0.0.1/Core_2_Level_3_") + str(random.randint(1, Max_Level_3)) + str(
                "/' /></my:has_parent_id>\n</rdf:Description>\n")

            f.write(body)
            i = i + 1
            k = k + 1
            if i > Max_Level_4:
                break
        f.write("\n</rdf:RDF>\n")
        f.close()
        spql.write(
            "\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_Model2_level4_" + str(FileNum) + "_.nq>;\n")
        k = 1
    spql.write("\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_static.nq>;\n")

# Add Object  definitions
    FileNum = 0
    i = 1
    k = 1
    while i <= Max_Objects_1:
        FileNum = FileNum + 1
        f = open(Model_path + filename + "_object_" + str(FileNum) + "_.nq", "at")
        f.write(header)
        f.write("\n<!--Objects definitions-->\n")
        while k <= Max_Step_1:
            body = str("<rdf:Description rdf:about='http://127.0.0.1/Object_") + str(i) + str("/'>\n<my:has_id>Object_") + str(i) + str("</my:has_id>\n<my:has_parent_id><rdf:Description rdf:about='http://127.0.0.1/Core_1_Level_4_") + str(random.randint(1, Max_Level_4)) + str("/' /></my:has_parent_id>\n</rdf:Description>\n")
            f.write(body)
            i = i + 1
            k = k + 1
            if i > Max_Objects_1:
                break
        f.write("\n</rdf:RDF>\n")
        f.close()
        spql.write("\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_object_" + str(FileNum) + "_.nq>;\n")
        k = 1

# Add Options  definitions
    FileNum = 0
    i = 1
    k = 1
    while i <= Max_Objects_2:
        FileNum = FileNum + 1
        f = open(Model_path + filename + "_option_" + str(FileNum) + "_.nq", "at")
        f.write(header)
        f.write("\n<!--Options definitions-->\n")
        while k <= Max_Step_1:
            body = str("<rdf:Description rdf:about='http://127.0.0.1/Option_") + str(i) + str(
                "/'>\n<my:has_id>Option_") + str(i) + str("</my:has_id>\n<my:has_parent_id><rdf:Description rdf:about='http://127.0.0.1/Core_2_Level_4_") + str(random.randint(1, Max_Level_4)) + str("/' /></my:has_parent_id>\n</rdf:Description>\n")
            f.write(body)
            i = i + 1
            if i > Max_Objects_2: break
            k = k + 1
        f.write("\n</rdf:RDF>\n")
        f.close()
        spql.write("\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_option_" + str(FileNum) + "_.nq>;\n")
        k = 1

 # Add Object-option links links Type-2  definitions
    FileNum = 0
    i = 1
    k = 1
    while i <= Max_Level_2:
        FileNum = FileNum + 1
        f = open(Model_path + filename + "_links_2_" + str(FileNum) + "_.nq", "at")
        f.write(header)
        f.write("\n<!--Add Object-option links Type-Hierarchy-->\n")
        while k <= Max_Step_1:
            body = str("<rdf:Description rdf:about='http://127.0.0.1/Core_1_Level_2_") + str(i) + str(
                "/'>\n<my:linked_to><rdf:Description rdf:about='http://127.0.0.1/Core_2_Level_2_") + str(i) + str("/' /></my:linked_to>\n</rdf:Description>\n")
            f.write(body)
            i = i + 1
            k = k + 1
            if i > Max_Level_2: break
        f.write("\n</rdf:RDF>\n")
        f.close()
        spql.write("\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_links_2_" + str(FileNum) + "_.nq>;\n")
        k = 1


    spql.close()

if __name__ == "__main__":
    createXML("KG_telecom")
