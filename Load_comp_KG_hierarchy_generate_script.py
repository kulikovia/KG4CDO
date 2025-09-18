import math
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


def createRDF_universal(filename, levels_number, elements_number, distribution_type, partial_models_number, linking_level, linking_rules, SPARQL_path, Model_path, IRI_prefix, isDynamic=False, start_date=None, end_date=None, dynamic_levels_elements_number=None, value_min=0, value_max=100):
    """
    Create RDF file.
    """
    Max_Level = []
    etalon_row = []
    Max_Level.append(0)
    if distribution_type == "uniform":
        for i in range(1, levels_number + 1):
            Max_Level.append(int(elements_number / levels_number))
    elif distribution_type == "linear":
        counter = 0
        for i in range(levels_number + 1):
            etalon_row.append(i)
            counter = counter + i
        add_factor = elements_number / counter
        for i in range(1, levels_number + 1):
            Max_Level.append(int(add_factor * etalon_row[i]))
    elif distribution_type == "quadratic":
        counter = 0
        for i in range(levels_number + 1):
            etalon_row.append(i ** 2)
            counter = counter + i ** 2
        add_factor = elements_number / counter
        for i in range(1, levels_number + 1):
            if int(add_factor * etalon_row[i]) == 0:
                Max_Level.append(1)
            else:
                Max_Level.append(int(add_factor * etalon_row[i]))
    elif distribution_type == "exponential":
        counter = 0
        for i in range(levels_number + 1):
            counter = counter + int(math.exp(i))
            etalon_row.append(int(math.exp(i)))
        add_factor = elements_number / counter
        for i in range(1, levels_number + 1):
            if int(add_factor * etalon_row[i]) == 0:
                Max_Level.append(1)
            else:
                Max_Level.append(int(add_factor * etalon_row[i]))
    else:
        print("Distribution type not supported")
        return -1

    #Tuning of the overall elements number by the changing last number elements number
    delta = elements_number - sum(Max_Level)
    Max_Level[len(Max_Level) - 1] = Max_Level[len(Max_Level) - 1] + delta

    print("Max_Level", Max_Level)

    #Open SPARQL file
    spql = open(Model_path + "sparql_script.spql", "wt")

    # Add header
    header = str("<?xml version='1.0' encoding='UTF-8'?>\n<rdf:RDF\nxmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'\nxmlns:vCard='http://www.w3.org/2001/vcard-rdf/3.0#'\nxmlns:my='" + IRI_prefix + "'\n>")

    f = open(Model_path + filename + "_static.rdf", "wt")
    f.write(header)

    # Models core definition
    for i in range(1, partial_models_number + 1):
        f.write("\n<!--Model " + str(i) + " Core definitions-->\n<rdf:Description rdf:about='" + IRI_prefix + "Core_" + str(i) + "_Level_0_element_1/'>\n<my:has_id>Core_" + str(i) + "</my:has_id>\n</rdf:Description>")
    f.write("\n</rdf:RDF>\n")
    f.close()

    # Model i hierarchy definition
    for i_model in range(1, partial_models_number + 1):
        for j in range(1, levels_number + 1):
            FileNum = 0
            i = 1
            k = 1
            while i <= Max_Level[j]:
                FileNum = FileNum + 1
                f = open(Model_path + filename + "_Model" + str(i_model) + "_level" + str(j) + "_" + str(FileNum) + "_.rdf", "at")
                f.write(header)
                f.write("\n<!--Objects definitions-->\n")
                while k <= Max_Step_1:
                    if Max_Level[j-1] == 0:
                        tmp_value = 1
                    else:
                        tmp_value = random.randint(1, Max_Level[j-1])
                    body = str("<rdf:Description rdf:about='" + IRI_prefix + "Core_" + str(i_model) + "_Level_" + str(j) + "_element_") + str(i) + str(
                        "/'>\n<my:has_id>Core_" + str(i_model) + "_Level_" + str(j) + "_element_") + str(i) + str(
                        "</my:has_id>\n<my:has_parent_id><rdf:Description rdf:about='" + IRI_prefix + "/Core_" + str(i_model) + "_Level_" + str(j-1) + "_element_" + str(tmp_value) + "/' /></my:has_parent_id>\n</rdf:Description>\n")

                    f.write(body)
                    i = i + 1
                    k = k + 1
                    if i > Max_Level[j]:
                        break
                f.write("\n</rdf:RDF>\n")
                f.close()
                spql.write("\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_Model" + str(i_model) + "_level" + str(j) + "_" + str(FileNum) + "_.rdf>;\n")
                k = 1

    rules = linking_rules.split(';')
    f = open(Model_path + filename + "_links_" + str(FileNum) + "_.rdf", "at")
    f.write(header)
    f.write("\n<!--Add cross=model links -->\n")
    for rule in rules:
        sub_rules = rule.split('-')
        # Add cross-model links  definitions
        FileNum = 0
        i = 1
        k = 1
        while i <= Max_Level[linking_level]:
            FileNum = FileNum + 1
            while k <= Max_Step_1:
                body = str("<rdf:Description rdf:about='" + IRI_prefix + "Core_" + str(sub_rules[0]) + "_Level_" + str(linking_level) + "_element_") + str(i) + str(
                    "/'>\n<my:linked_to><rdf:Description rdf:about='" + IRI_prefix + "Core_" + str(sub_rules[1]) + "_Level_" + str(linking_level) + "_element_") + str(i) + str("/' /></my:linked_to>\n</rdf:Description>\n")
                f.write(body)
                i = i + 1
                k = k + 1
                if i > Max_Level[linking_level]: break
            k = 1
    f.write("\n</rdf:RDF>\n")
    f.close()
    spql.write("\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_links_" + str(FileNum) + "_.rdf>;\n")

    if isDynamic == True:
        d1 = datetime.strptime(start_date + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        d2 = datetime.strptime(end_date + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
        dynamic_levels_elements_number_list = dynamic_levels_elements_number.split(';')
        FileNum = 0
        counter = 1
        for item in dynamic_levels_elements_number_list:
            sub_item = item.split('-')
            # Add dynamic items
            i = 1
            k = 1
            while i <= Max_Level[linking_level]:
                FileNum = FileNum + 1
                f = open(Model_path + filename + "_dynamic_data_" + str(FileNum) + "_.rdf", "at")
                f.write(header)
                f.write("\n<!--Add dynamic data -->\n")
                while k <= Max_Step_1:
                    body = "<rdf:Description rdf:about='" + IRI_prefix + "Core_Parameter_" + str(counter) + "/'>\n<rdf:type>:ParameterValue</rdf:type>\n<:parameter_timestamp rdf:datatype='http://www.w3.org/2001/XMLSchema#datetime'>" + str(random_date(d1, d2).strftime("%Y-%m-%dT%H:%M:%S")) + "</:parameter_timestamp>\n<:has_parameter_type>:CoreParameter</:has_parameter_type>\n<:parameter_detailes>\n<rdf:Description>\n<rdf:type>rdf:statement</rdf:type>\n<rdf:predicat>:parameter_value</rdf:predicat>\n<rdf:subject><rdf:Description rdf:about='" + IRI_prefix + "Core_" + str(random.randint(1, partial_models_number)) + "_Level_" + str(sub_item[0]) + "_element_" + str(random.randint(sum(Max_Level[0:int(sub_item[0])]), sum(Max_Level[0:int(sub_item[0]) + 1]))) + "/'></rdf:Description></rdf:subject>\n<rdf:object>" + str(random.randint(value_min, value_max)) + "</rdf:object>\n</rdf:Description>\n</:parameter_detailes>\n</rdf:Description>\n\n"
                    f.write(body)
                    i = i + 1
                    k = k + 1
                    counter = counter + 1
                    if i > int(sub_item[1]): break
                k = 1
        f.write("\n</rdf:RDF>\n")
        f.close()
        spql.write("\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_dynamic_data_" + str(FileNum) + "_.rdf>;\n")

    spql.close()


def createRDF_domain(filename, Levels, elements_number, distribution_type, Models, linking_level, linking_rules, SPARQL_path, Model_path, IRI_prefix, isDynamic=False, start_date=None, end_date=None, dynamic_levels_elements_number=None, value_min=0, value_max=100):
    """
    Create RDF file.
    """
    Max_Level = []
    etalon_row = []
    Max_Level.append(0)
    levels_number = len(Levels[0])
    if distribution_type == "uniform":
        for i in range(1, levels_number + 1):
            Max_Level.append(int(elements_number / levels_number))
    elif distribution_type == "linear":
        counter = 0
        for i in range(levels_number + 1):
            etalon_row.append(i)
            counter = counter + i
        add_factor = elements_number / counter
        for i in range(1, levels_number + 1):
            Max_Level.append(int(add_factor * etalon_row[i]))
    elif distribution_type == "quadratic":
        counter = 0
        for i in range(levels_number + 1):
            etalon_row.append(i ** 2)
            counter = counter + i ** 2
        add_factor = elements_number / counter
        for i in range(1, levels_number + 1):
            if int(add_factor * etalon_row[i]) == 0:
                Max_Level.append(1)
            else:
                Max_Level.append(int(add_factor * etalon_row[i]))
    elif distribution_type == "exponential":
        counter = 0
        for i in range(levels_number + 1):
            counter = counter + int(math.exp(i))
            etalon_row.append(int(math.exp(i)))
        add_factor = elements_number / counter
        for i in range(1, levels_number + 1):
            if int(add_factor * etalon_row[i]) == 0:
                Max_Level.append(1)
            else:
                Max_Level.append(int(add_factor * etalon_row[i]))
    else:
        print("Distribution type not supported")
        return -1

    #Tuning of the overall elements number by the changing last number elements number
    delta = elements_number - sum(Max_Level)
    Max_Level[len(Max_Level) - 1] = Max_Level[len(Max_Level) - 1] + delta

    print("Max_Level", Max_Level)

    #Open SPARQL file
    spql = open(Model_path + "sparql_script.spql", "wt")

    # Add header
    header = str("<?xml version='1.0' encoding='UTF-8'?>\n<rdf:RDF\nxmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'\nxmlns:vCard='http://www.w3.org/2001/vcard-rdf/3.0#'\nxmlns:my='http://127.0.0.1/bg/ont/test1#'\n>")

    f = open(Model_path + filename + "_static.rdf", "wt")
    f.write(header)

    # Models core definition
    for i_model in Models:
        f.write("\n<!--" + str(i_model) + " Core definitions-->\n<rdf:Description rdf:about='" + IRI_prefix + "Core_" + str(i_model) + "_Level_0_element_1/'>\n<my:has_id>Core_" + str(i_model) + "</my:has_id>\n</rdf:Description>")
    f.write("\n</rdf:RDF>\n")
    f.close()

    # Model i hierarchy definition
    l = 0
    for i_model in Models:
        for j in range(1, levels_number + 1):
            FileNum = 0
            i = 1
            k = 1
            while i <= Max_Level[j]:
                FileNum = FileNum + 1
                f = open(Model_path + filename + "_" + str(i_model) + "_level" + str(j) + "_" + str(FileNum) + "_.rdf", "at")
                f.write(header)
                f.write("\n<!--Objects definitions-->\n")
                while k <= Max_Step_1:
                    if Max_Level[j-1] == 0:
                        tmp_value = 1
                    else:
                        tmp_value = random.randint(1, Max_Level[j-1])
                    body = str("<rdf:Description rdf:about='" + IRI_prefix + str(i_model) + "_" + str(Levels[l][j - 1]) + "_") + str(i) + str(
                        "/'>\n<my:has_id>" + str(i_model) + "_" + str(Levels[l][j - 1]) + "_") + str(i) + str(
                        "</my:has_id>\n<my:has_parent_id><rdf:Description rdf:about='" + IRI_prefix + str(i_model) + "_" + str(Levels[l][j - 2]) + "_" + str(tmp_value) + "/' /></my:has_parent_id>\n</rdf:Description>\n")

                    f.write(body)
                    i = i + 1
                    k = k + 1
                    if i > Max_Level[j]:
                        break
                f.write("\n</rdf:RDF>\n")
                f.close()
                spql.write("\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_" + str(i_model) + "_level" + str(j) + "_" + str(FileNum) + "_.rdf>;\n")
                k = 1
        l = l + 1
    rules = linking_rules.split(';')
    f = open(Model_path + filename + "_links_" + str(FileNum) + "_.rdf", "at")
    f.write(header)
    f.write("\n<!--Add cross=model links -->\n")
    for rule in rules:
        sub_rules = rule.split('-')
        # Add cross-model links  definitions
        FileNum = 0
        i = 1
        k = 1
        while i <= Max_Level[linking_level]:
            FileNum = FileNum + 1
            while k <= Max_Step_1:
                body = "<rdf:Description rdf:about='" + IRI_prefix + str(Models[int(sub_rules[0]) - 1]) + "_" + str(Levels[int(sub_rules[0]) - 1][int(linking_level) - 1]) + "_" + str(i) + "/'>\n<my:linked_to><rdf:Description rdf:about='" + IRI_prefix + str(Models[int(sub_rules[1]) - 1]) + "_" + str(Levels[int(sub_rules[1]) - 1][int(linking_level) - 1]) + "_" + str(i) + str("/' /></my:linked_to>\n</rdf:Description>\n")
                f.write(body)
                i = i + 1
                k = k + 1
                if i > Max_Level[linking_level]: break
            k = 1
    f.write("\n</rdf:RDF>\n")
    f.close()
    spql.write("\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_links_" + str(FileNum) + "_.rdf>;\n")

    if isDynamic == True:
        d1 = datetime.strptime(start_date + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        d2 = datetime.strptime(end_date + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
        dynamic_levels_elements_number_list = dynamic_levels_elements_number.split(';')
        FileNum = 0
        counter = 1
        for item in dynamic_levels_elements_number_list:
            sub_item = item.split('-')
            # Add dynamic items
            i = 1
            k = 1
            while i <= Max_Level[linking_level]:
                FileNum = FileNum + 1
                f = open(Model_path + filename + "_dynamic_data_" + str(FileNum) + "_.rdf", "at")
                f.write(header)
                f.write("\n<!--Add dynamic data -->\n")
                while k <= Max_Step_1:
                    body = "<rdf:Description rdf:about='" + IRI_prefix + "Core_Parameter_" + str(counter) + "/'>\n<rdf:type>:ParameterValue</rdf:type>\n<:parameter_timestamp rdf:datatype='http://www.w3.org/2001/XMLSchema#datetime'>" + str(random_date(d1, d2).strftime("%Y-%m-%dT%H:%M:%S")) + "</:parameter_timestamp>\n<:has_parameter_type>:CoreParameter</:has_parameter_type>\n<:parameter_detailes>\n<rdf:Description>\n<rdf:type>rdf:statement</rdf:type>\n<rdf:predicat>:parameter_value</rdf:predicat>\n<rdf:subject><rdf:Description rdf:about='" + IRI_prefix + "Core_" + str(random.randint(1, partial_models_number)) + "_Level_" + str(sub_item[0]) + "_element_" + str(random.randint(sum(Max_Level[0:int(sub_item[0])]), sum(Max_Level[0:int(sub_item[0]) + 1]))) + "/'></rdf:Description></rdf:subject>\n<rdf:object>" + str(random.randint(value_min, value_max)) + "</rdf:object>\n</rdf:Description>\n</:parameter_detailes>\n</rdf:Description>\n\n"
                    f.write(body)
                    i = i + 1
                    k = k + 1
                    counter = counter + 1
                    if i > int(sub_item[1]): break
                k = 1
        f.write("\n</rdf:RDF>\n")
        f.close()
        spql.write("\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_dynamic_data_" + str(FileNum) + "_.rdf>;\n")

    spql.close()



if __name__ == "__main__":
    Models = ['Access_Network_Subsystem', 'Core_Network_Subsystem', 'Transmission_Network_Subsystem',
              'Base_Station_Subsystem', 'Network_Management_Subsystem', 'Billing_Subsystem',
              'User_Management_Subsystem', 'Security_Subsystem', 'Service_Subsystem',
              'Operations_and_Maintenance_Subsystem']

    Levels = [['Geographic_region', 'Geo_sub-region_Level_1', 'Geo_sub-region_Level_2', 'Geo_sub-region_Level_3',
               'Accessed_Device_Layer_1_Unit_(connection_layer)', 'Accessed_Device_Layer_2_Unit',
               'Accessed_Device_Layer_3_Unit', 'Accessed_Device_Layer_4_Unit', 'Accessed_Device_Layer_5_Unit',
               'Accessed_Device'],
              ['Domain', 'Sub-Domain_Level_1_Unit', 'Sub-Domain_Level_2_Unit', 'Sub-Domain_Level_3_Unit',
               'Sub-Domain_Level_4_Unit_(connection_layer)', 'Sub-Domain_Level_5_Unit', 'Sub-Domain_Level_6_Unit',
               'Sub-Domain_Level_7_Unit', 'Sub-Domain_Level_8_Unit', 'Core_Device'],
              ['Network_Type', 'Network_Sub-Type_Level_1', 'Network_Sub-Type_Level_2', 'Network_Sub-Type_Level_3',
               'Network_Sub-Type_Level_4_(connection_level)', 'Network_Sub-Type_Level_5', 'Network_Sub-Type_Level_6',
               'Network_Sub-Type_Level_7', 'Network_Sub-Type_Level_8', 'Transmission_Device'],
              ['Geographic_region', 'Geo_sub-region_Level_1', 'Geo_sub-region_Level_2', 'Geo_sub-region_Level_3',
               'Base_Station_Layer_1_Unit_(connection_layer)', 'Base_Station_Layer_2_Unit', 'Base_Station_Layer_3_Unit',
               'Base_Station_Layer_4_Unit', 'Base_Station_Layer_5_Unit', 'Base_Station'],
              ['Management_Domain', 'Management_Sub-Domain_Level_1', 'Management_Sub-Domain_Level_2',
               'Management_Sub-Domain_Level_3', 'Management_Sub-Domain_Level_4_(connection_level)',
               'Management_Sub-Domain_Level_5', 'Management_Sub-Domain_Level_6', 'Management_Sub-Domain_Level_7',
               'Management_Sub-Domain_Level_8', 'Management_device_or_system'],
              ['Tariff_group', 'Tariff_sub-group_Level_1', 'Tariff_sub-group_Level_2', 'Tariff_sub-group_Level_3',
               'Tariff_sub-group_Level_4_(connection_layer)', 'Tariff_sub-group_Level_5', 'Tariff_sub-group_Level_6',
               'Tariff_sub-group_Level_7', 'Tariff_sub-group_Level_8', 'User_account'],
              ['User_Management_Domain', 'User_Management_Sub-Domain_Level_1', 'User_Management_Sub-Domain_Level_2',
               'User_Management_Sub-Domain_Level_3', 'User_Management_Sub-Domain_Level_4_(connection_level)',
               'User_Management_Sub-Domain_Level_5', 'User_Management_Sub-Domain_Level_6',
               'User_Management_Sub-Domain_Level_7', 'User_Management_Sub-Domain_Level_8', 'User_Management_item'],
              ['Security_Domain', 'Security_Sub-Domain_Level_1', 'Security_Sub-Domain_Level_2',
               'Security_Sub-Domain_Level_3', 'Security_Sub-Domain_Level_4_(connection_level)',
               'Security_Sub-Domain_Level_5', 'Security_Sub-Domain_Level_6', 'Security_Sub-Domain_Level_7',
               'Security_Sub-Domain_Level_8', 'Security_Group'],
              ['Service_Domain', 'Service_Sub-Domain_Level_1', 'Service_Sub-Domain_Level_2',
               'Service_Sub-Domain_Level_3', 'Service_Sub-Domain_Level_4_(connection_level)',
               'Service_Sub-Domain_Level_5', 'Service_Sub-Domain_Level_6', 'Service_Sub-Domain_Level_7',
               'Service_Sub-Domain_Level_8', 'Service'],
              ['O._and_M._Domain', 'O._and_M._Sub-Domain_Level_1', 'O._and_M._Sub-Domain_Level_2',
               'O._and_M._Sub-Domain_Level_3', 'O._and_M._Sub-Domain_Level_4_(connection_level)',
               'O._and_M._Sub-Domain_Level_5', 'O._and_M._Sub-Domain_Level_6', 'O._and_M._Sub-Domain_Level_7',
               'O._and_M._Sub-Domain_Level_8', 'Operation'],
              ]

    #createRDF_universal("KG_data", 6,100,"exponential", 3, 3, "1-2;2-3", "C:/Blazegraph/Load", "Hierarchy_model/", "http://127.0.0.1/ont_test#",False, '2025-08-01', '2025-08-02', '2-10;3-10;4-10')

    #createRDF_domain("KG_data", Levels, 100000, "exponential", Models, 5, "1-2;2-3;3-4;4-5;5-6;6-7;7-8;8-9;9-10", "C:/Blazegraph/Load", "Hierarchy_model/", "http://127.0.0.1/ont_test#",False, '2025-08-01', '2025-08-02', '2-10;3-10;4-10')
