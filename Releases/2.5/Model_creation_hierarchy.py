import random
import math

def create_uni_model(levels_number, elements_number, distribution_type, partial_models_number, linking_level, linking_rules):

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
    for i_model in range(1, partial_models_number + 1):
        body = "Model_" + str(i_model) + ",Model_" + str(i_model) + "_Element_level_0,0," + "Model_" + str(i_model) + "_Core_node,,0\n"
        model_csv.write(body)
        facts1_csv.write(body)
        facts2_csv.write(body)
        i = 1
        for j in range(1, levels_number + 1):
            level_counter = 1
            while level_counter <= Max_Level[j]:
                if Max_Level[j - 1] == 0:
                    tmp_value = 0
                else:
                    tmp_summa = 0
                    for tmp_level in range(0, j - 2):
                        tmp_summa = tmp_summa + Max_Level[tmp_level]
                    tmp_value = random.randint(tmp_summa, tmp_summa + Max_Level[j - 1])
                body = "Model_" + str(i_model) + ",Model_" + str(i_model) + "_Element_level_" + str(j) + "," + str(i) + ",Model_" + str(i) + "_Element_level_" + str(j) +"_" + str(i) + "," + str(tmp_value) + "," + str(j) + "\n"
                model_csv.write(body)
                facts1_csv.write(body)
                facts2_csv.write(body)
                i = i + 1
                level_counter = level_counter + 1
                if level_counter > Max_Level[j]:
                    break
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
            body = "Model_" + str(sub_rules[0]) + "," + str(i) + ",Model_" + str(sub_rules[0]) + "_Element_level_" + str(linking_level) + "_" + str(i) + ",Model_" + str(sub_rules[1]) + "," + str(i) + ",Model_" + str(sub_rules[1]) + "_Element_level_" + str(linking_level) + "_" + str(i) + ",connected\n"
            f.write(body)

    f.close()

    return 1

def create_uni_model_for_One_level(levels_number, elements_number, distribution_type, partial_models_number, linking_level, linking_rules, selected_level):

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
    for i_model in range(1, partial_models_number + 1):
        body = "Model_" + str(i_model) + ",Model_" + str(i_model) + "_Element_level_0,0," + "Model_" + str(i_model) + "_Core_node,,0\n"
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
            body = "Model_" + str(i_model) + ",Model_" + str(i_model) + "_Element_level_" + str(selected_level) + "," + str(i) + ",Model_" + str(i) + "_Element_level_" + str(selected_level) +"_" + str(i) + "," + str(tmp_value) + "," + str(selected_level) + "\n"
            model_csv.write(body)
            facts1_csv.write(body)
            facts2_csv.write(body)
            i = i + 1
            level_counter = level_counter + 1
            if level_counter > Max_Level[selected_level]:
                break
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
            body = "Model_" + str(sub_rules[0]) + "," + str(i) + ",Model_" + str(sub_rules[0]) + "_Element_level_" + str(linking_level) + "_" + str(i) + ",Model_" + str(sub_rules[1]) + "," + str(i) + ",Model_" + str(sub_rules[1]) + "_Element_level_" + str(linking_level) + "_" + str(i) + ",connected\n"
            f.write(body)

    f.close()

    return 1

def create_uni_model_for_List_levels(levels_number, elements_number, distribution_type, partial_models_number, linking_level, linking_rules, levels_list):

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
    for i_model in range(1, partial_models_number + 1):
        body = "Model_" + str(i_model) + ",Model_" + str(i_model) + "_Element_level_0,0," + "Model_" + str(i_model) + "_Core_node,,0\n"
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
                body = "Model_" + str(i_model) + ",Model_" + str(i_model) + "_Element_level_" + str(j) + "," + str(i) + ",Model_" + str(i) + "_Element_level_" + str(j) +"_" + str(i) + "," + str(tmp_value) + "," + str(j) + "\n"
                model_csv.write(body)
                facts1_csv.write(body)
                facts2_csv.write(body)
                i = i + 1
                level_counter = level_counter + 1
                if level_counter > Max_Level[int(j)]:
                    break
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
            body = "Model_" + str(sub_rules[0]) + "," + str(i) + ",Model_" + str(sub_rules[0]) + "_Element_level_" + str(linking_level) + "_" + str(i) + ",Model_" + str(sub_rules[1]) + "," + str(i) + ",Model_" + str(sub_rules[1]) + "_Element_level_" + str(linking_level) + "_" + str(i) + ",connected\n"
            f.write(body)

    f.close()

    return 1



if __name__ == "__main__":
    #create_uni_model(5,50,"exponential", 2, 3, "1-2")

    #create_uni_model_for_One_level(10, 100000, "exponential", 5, 5, "1-2;2-3;3-4;4-5", 1)
    create_uni_model_for_List_levels(5, 50, "exponential", 1, 5, "1-2;2-3;3-4;4-5;5-6;6-7;7-8;8-9;9-10", "9;10")