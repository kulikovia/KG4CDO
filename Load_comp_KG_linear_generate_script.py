import xml.etree.ElementTree as xml
import random
from random import randrange
from datetime import datetime
from datetime import timedelta

Max_Step_1 = 100000
Max_Step_2 = 50000

def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def createRDF_universal_One_level(filename, partial_models_number, elements_number, linking_rules, SPARQL_path, Model_path, IRI_prefix, isDynamic=False, start_date=None, end_date=None, value_min=0, value_max=100, elements_number_dynamic=100):
    """
    Создаем XML файл.
    """
#Open SPARQL file
    spql = open(Model_path + "sparql_script.spql", "wt")

# Add header
    header = str("<?xml version='1.0' encoding='UTF-8'?>\n<rdf:RDF\nxmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'\nxmlns:vCard='http://www.w3.org/2001/vcard-rdf/3.0#'\nxmlns:my='" + IRI_prefix + "'\n>")

    f = open(Model_path + filename + "_static.nq", "wt")
    f.write(header)

# Models hierarchy definition
# Add Core definitions
    for i_model in range(1, partial_models_number + 1):
        f.write("\n<!--Model Core definitions-->\n<rdf:Description rdf:about='" + IRI_prefix + "Core_" + str(i_model) + "_element_0/'>\n<my:has_id>Core_" + str(i_model) + "</my:has_id>\n</rdf:Description>")

    f.write("\n</rdf:RDF>\n")
    f.close()
    spql.write("\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_static.nq>;\n")

    # Model i hierarchy definition
    FileNum = 0
    for i_model in range(1, partial_models_number + 1):
        i = 1
        k = 1
        while i <= elements_number:
            FileNum = FileNum + 1
            f = open(Model_path + filename + "_object_" + str(FileNum) + "_.nq", "at")
            f.write(header)
            f.write("\n<!--Objects definitions-->\n")
            while k <= Max_Step_1:
                body = "<rdf:Description rdf:about='" + IRI_prefix + "Core_" + str(i_model) + "_element_" + str(i) + "/'>\n<my:has_id>Core_" + str(i_model) + "_element_" + str(i) + "</my:has_id>\n<my:has_parent_id>Core_" + str(i_model) + "/'></my:has_parent_id>\n</rdf:Description>\n"
                f.write(body)
                i = i + 1
                k = k + 1
                if i > elements_number: break
            f.write("\n</rdf:RDF>\n")
            f.close()
            spql.write("\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_object_" + str(FileNum) + "_.nq>;\n")
            k = 1


    rules = linking_rules.split(';')

    # Add cross-model links  definitions
    FileNum = 0
    i = 1
    k = 1
    for rule in rules:
        sub_rules = rule.split('-')
        while i <= elements_number:
            FileNum = FileNum + 1
            f = open(Model_path + filename + "_links_" + str(FileNum) + "_.rdf", "at")
            f.write(header)
            f.write("\n<!--Add cross=model links -->\n")
            while k <= Max_Step_1:
                body = "<rdf:Description rdf:about='" + IRI_prefix + "Core_" + str(sub_rules[0]) + "_element_" + str(i) + "/'>\n<my:linked_to><rdf:Description rdf:about='" + IRI_prefix + "Core_" + str(sub_rules[1]) + "_element_" + str(i) + "/' /></my:linked_to>\n</rdf:Description>\n"
                f.write(body)
                i = i + 1
                k = k + 1
                if i > elements_number: break
            k = 1
    f.write("\n</rdf:RDF>\n")
    f.close()
    spql.write("\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_links_" + str(FileNum) + "_.rdf>;\n")

    if isDynamic == True:
        d1 = datetime.strptime(start_date + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        d2 = datetime.strptime(end_date + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
        FileNum = 0
        counter = 1
        # Add dynamic items
        i = 1
        k = 1
        while i <= elements_number_dynamic:
            FileNum = FileNum + 1
            f = open(Model_path + filename + "_dynamic_data_" + str(FileNum) + "_.rdf", "at")
            f.write(header)
            f.write("\n<!--Add dynamic data -->\n")
            while k <= Max_Step_1:
                body = "<rdf:Description rdf:about='" + IRI_prefix + "Core_Parameter_" + str(counter) + "/'>\n<rdf:type>:ParameterValue</rdf:type>\n<my:parameter_timestamp rdf:datatype='http://www.w3.org/2001/XMLSchema#datetime'>" + str(random_date(d1, d2).strftime("%Y-%m-%dT%H:%M:%S")) + "</my:parameter_timestamp>\n<my:has_parameter_type>my:CoreParameter</my:has_parameter_type>\n<my:parameter_detailes>\n<rdf:Description>\n<rdf:type>rdf:statement</rdf:type>\n<rdf:predicat>my:parameter_value</rdf:predicat>\n<rdf:subject><rdf:Description rdf:about='" + IRI_prefix + "Core_" + str(random.randint(1, partial_models_number)) + "_element_" + str(random.randint(1, elements_number)) + "/'></rdf:Description></rdf:subject>\n<rdf:object>" + str(random.randint(value_min, value_max)) + "</rdf:object>\n</rdf:Description>\n</my:parameter_detailes>\n</rdf:Description>\n\n"
                f.write(body)
                i = i + 1
                k = k + 1
                counter = counter + 1
                if i > elements_number_dynamic: break
            k = 1
        f.write("\n</rdf:RDF>\n")
        f.close()
        spql.write("\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_dynamic_data_" + str(FileNum) + "_.rdf>;\n")

    spql.close()


if __name__ == "__main__":
    createRDF_universal_One_level("KG_data", 5, 10, "1-2;2-3;3-4;4-5", "C:/Blazegraph/Load", "Linear_model/", "http://127.0.0.1/ont_test#", isDynamic=True, start_date='2025-09-10', end_date='2025-09-18', value_min=0, value_max=100, elements_number_dynamic=100)
