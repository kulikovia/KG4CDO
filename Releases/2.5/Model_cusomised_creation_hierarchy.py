import random
import math

def create_cust_model(Levels, elements_number, distribution_type, Models, linking_level, linking_rules):

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

    # Tuning of the overall elements number by the changing last number elements number
    delta = elements_number - sum(Max_Level)
    Max_Level[len(Max_Level) - 1] = Max_Level[len(Max_Level) - 1] + delta

    # Open csv file
    model_csv = open("TMP/Test_model.csv", "wt")
    facts1_csv = open("TMP/Test_facts1.csv", "wt")
    facts2_csv = open("TMP/Test_facts2.csv", "wt")
    header_mod = 'MODEL_TYPE,NODE_TYPE,ID,NAME,PARENT_ID,LEVEL_NUM\n'
    header_fact = 'MODEL_TYPE,NODE_TYPE,FACT_ID,NAME,PARENT_ID,LEVEL_NUM\n'

    # Add header and template
    model_csv.write(header_mod)
    facts1_csv.write(header_fact)
    facts2_csv.write(header_fact)

    # Model i hierarchy definition
    k = 0
    for i_model in Models:
        body = str(i_model) + "," + str(i_model) + "_Element_level_0,0," + str(i_model) + "_Core_node,,0\n"
        model_csv.write(body)
        facts1_csv.write(body)
        facts2_csv.write(body)
        i = 1
        for j in range(1, len(Levels) + 1):
            level_counter = 1
            while level_counter <= Max_Level[j]:
                if Max_Level[j - 1] == 0:
                    tmp_value = 0
                else:
                    tmp_summa = 0
                    for tmp_level in range(0, j - 2):
                        tmp_summa = tmp_summa + Max_Level[tmp_level]
                    tmp_value = random.randint(tmp_summa, tmp_summa + Max_Level[j - 1])
                body = str(i_model) + "," + str(i_model) + "_" + str(Levels[k][j-1]) + "," + str(i) + "," + str(i_model) + "_" + str(Levels[k][j-1]) +"_" + str(i) + "," + str(tmp_value) + "," + str(j) + "\n"
                model_csv.write(body)
                facts1_csv.write(body)
                facts2_csv.write(body)
                i = i + 1
                level_counter = level_counter + 1
                if level_counter > Max_Level[j]:
                    break
        k = k + 1
    #Close file
    model_csv.close()
    facts1_csv.close()
    facts2_csv.close()

    rules = linking_rules.split(';')
    f = open("TMP/Links_rules.csv", "wt")
    header = "SRC_MODEL,SRC_ID,SRC_NAME,DIST_MODEL,DIST_ID,DIST_NAME,RULE\n"
    f.write(header)
    tmp_summa = 0
    for tmp_level in range(0, linking_level):
        tmp_summa = tmp_summa + Max_Level[tmp_level]
    print('Max_Level=', Max_Level)
    print('tmp_summa=', tmp_summa)
    for rule in rules:
        sub_rules = rule.split('-')
        # Add cross-model links  definitions
        for i in range(tmp_summa + 1, tmp_summa + 1 + Max_Level[linking_level]):
            #print('i=',i)
            body = str(Models[int(sub_rules[0]) - 1]) + "," + str(i) + "," + str(Models[int(sub_rules[0]) - 1]) + "_" + str(Levels[linking_level - 1][j-1]) + "_" + str(i) + "," + str(Models[int(sub_rules[1]) - 1]) + "," + str(i) + "," + str(Models[int(sub_rules[1]) - 1]) + "_" + str(Levels[linking_level - 1][j-1]) + "_" + str(i) + ",connected\n"

            f.write(body)

    f.close()

    return 1

def create_cust_model_for_One_level(Levels, elements_number, distribution_type, Models, linking_level, linking_rules, selected_level):

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

    # Tuning of the overall elements number by the changing last number elements number
    delta = elements_number - sum(Max_Level)
    Max_Level[len(Max_Level) - 1] = Max_Level[len(Max_Level) - 1] + delta

    # Open csv file
    model_csv = open("TMP/Test_model.csv", "wt")
    facts1_csv = open("TMP/Test_facts1.csv", "wt")
    facts2_csv = open("TMP/Test_facts2.csv", "wt")
    header_mod = 'MODEL_TYPE,NODE_TYPE,ID,NAME,PARENT_ID,LEVEL_NUM\n'
    header_fact = 'MODEL_TYPE,NODE_TYPE,FACT_ID,NAME,PARENT_ID,LEVEL_NUM\n'

    # Add header and template
    model_csv.write(header_mod)
    facts1_csv.write(header_fact)
    facts2_csv.write(header_fact)

    # Model i hierarchy definition
    for i_model in Models:
        body = str(i_model) + "," + str(i_model) + "_Element_level_0,0," + str(i_model) + "_Core_node,,0\n"
        model_csv.write(body)
        facts1_csv.write(body)
        facts2_csv.write(body)
        i = 1
        level_counter = 1
        while level_counter <= Max_Level[selected_level]:
            if Max_Level[selected_level - 1] == 0:
                tmp_value = 0
            else:
                tmp_summa = 0
                for tmp_level in range(0, selected_level - 2):
                    tmp_summa = tmp_summa + Max_Level[tmp_level]
                tmp_value = random.randint(tmp_summa, tmp_summa + Max_Level[selected_level - 1])
            body = str(i_model) + "," + str(i_model) + "_" + str(Levels[k][selected_level - 1]) + "," + str(i) + "," + str(i_model) + "_" + str(Levels[k][selected_level - 1]) + "_" + str(i) + "," + str(tmp_value) + "," + str(selected_level) + "\n"
            model_csv.write(body)
            facts1_csv.write(body)
            facts2_csv.write(body)
            i = i + 1
            level_counter = level_counter + 1
            if level_counter > Max_Level[selected_level]:
                break
        k = k + 1
    #Close file
    model_csv.close()
    facts1_csv.close()
    facts2_csv.close()

    rules = linking_rules.split(';')
    f = open("TMP/Links_rules.csv", "wt")
    header = "SRC_MODEL,SRC_ID,SRC_NAME,DIST_MODEL,DIST_ID,DIST_NAME,RULE\n"
    f.write(header)
    tmp_summa = 0
    for tmp_level in range(0, linking_level):
        tmp_summa = tmp_summa + Max_Level[tmp_level]
    print('Max_Level=', Max_Level)
    print('tmp_summa=', tmp_summa)
    for rule in rules:
        sub_rules = rule.split('-')
        # Add cross-model links  definitions
        for i in range(tmp_summa + 1, tmp_summa + 1 + Max_Level[linking_level]):
            #print('i=',i)
            body = str(Models[int(sub_rules[0]) - 1]) + "," + str(i) + "," + str(Models[int(sub_rules[0]) - 1]) + "_" + str(Levels[linking_level - 1][j-1]) + "_" + str(i) + "," + str(Models[int(sub_rules[1]) - 1]) + "," + str(i) + "," + str(Models[int(sub_rules[1]) - 1]) + "_" + str(Levels[linking_level - 1][j-1]) + "_" + str(i) + ",connected\n"
            f.write(body)

    f.close()

    return 1

def create_cust_model_for_List_levels(Levels, elements_number, distribution_type, Models, linking_level, linking_rules, levels_list):

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

    # Tuning of the overall elements number by the changing last number elements number
    delta = elements_number - sum(Max_Level)
    Max_Level[len(Max_Level) - 1] = Max_Level[len(Max_Level) - 1] + delta

    # Open csv file
    model_csv = open("TMP/Test_model.csv", "wt")
    facts1_csv = open("TMP/Test_facts1.csv", "wt")
    facts2_csv = open("TMP/Test_facts2.csv", "wt")
    header_mod = 'MODEL_TYPE,NODE_TYPE,ID,NAME,PARENT_ID,LEVEL_NUM\n'
    header_fact = 'MODEL_TYPE,NODE_TYPE,FACT_ID,NAME,PARENT_ID,LEVEL_NUM\n'

    # Add header and template
    model_csv.write(header_mod)
    facts1_csv.write(header_fact)
    facts2_csv.write(header_fact)

    # Model i hierarchy definition
    levels = levels_list.split(';')
    for i_model in Models:
        body = str(i_model) + "," + str(i_model) + "_Element_level_0,0," + str(i_model) + "_Core_node,,0\n"
        model_csv.write(body)
        facts1_csv.write(body)
        facts2_csv.write(body)
        i = 1
        for j in levels:
            level_counter = 1
            while level_counter <= Max_Level[int(j)]:
                if Max_Level[int(j) - 1] == 0:
                    tmp_value = 0
                else:
                    tmp_summa = 0
                    for tmp_level in range(0, int(j) - 2):
                        tmp_summa = tmp_summa + Max_Level[tmp_level]
                    tmp_value = random.randint(tmp_summa, tmp_summa + Max_Level[int(j) - 1])
                body = str(i_model) + "," + str(i_model) + "_" + str(Levels[k][j - 1]) + "," + str(i) + "," + str(i_model) + "_" + str(Levels[k][j - 1]) + "_" + str(i) + "," + str(tmp_value) + "," + str(j) + "\n"
                model_csv.write(body)
                facts1_csv.write(body)
                facts2_csv.write(body)
                i = i + 1
                level_counter = level_counter + 1
                if level_counter > Max_Level[int(j)]:
                    break
        k = k + 1
    #Close file
    model_csv.close()
    facts1_csv.close()
    facts2_csv.close()

    rules = linking_rules.split(';')
    f = open("TMP/Links_rules.csv", "wt")
    header = "SRC_MODEL,SRC_ID,SRC_NAME,DIST_MODEL,DIST_ID,DIST_NAME,RULE\n"
    f.write(header)
    tmp_summa = 0
    for tmp_level in range(0, linking_level):
        tmp_summa = tmp_summa + Max_Level[tmp_level]
    print('Max_Level=', Max_Level)
    print('tmp_summa=', tmp_summa)
    for rule in rules:
        sub_rules = rule.split('-')
        # Add cross-model links  definitions
        for i in range(tmp_summa + 1, tmp_summa + 1 + Max_Level[linking_level]):
            #print('i=',i)
            body = str(Models[int(sub_rules[0]) - 1]) + "," + str(i) + "," + str(Models[int(sub_rules[0]) - 1]) + "_" + str(Levels[linking_level - 1][j-1]) + "_" + str(i) + "," + str(Models[int(sub_rules[1]) - 1]) + "," + str(i) + "," + str(Models[int(sub_rules[1]) - 1]) + "_" + str(Levels[linking_level - 1][j-1]) + "_" + str(i) + ",connected\n"
            f.write(body)

    f.close()

    return 1



if __name__ == "__main__":
    Models = ['Access_Network_Subsystem', 'Core_Network_Subsystem', 'Transmission_Network_Subsystem', 'Base_Station_Subsystem', 'Network_Management_Subsystem', 'Billing_Subsystem', 'User_Management_Subsystem', 'Security_Subsystem', 'Service_Subsystem', 'Operations_and_Maintenance_Subsystem']

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

    #create_cust_model(Levels,100000,"exponential", Models, 5, "1-2;2-3;3-4;4-5;5-6;6-7;7-8;8-9;9-10")

    #create_cust_model_for_One_level(Levels, 100000, "exponential", Models, 5, "1-2;2-3;3-4;4-5", 1)

    #create_cust_model_for_List_levels(Levels, 100000, "exponential", Models, 5, "1-2;2-3;3-4;4-5;5-6;6-7;7-8;8-9;9-10", "9;10")