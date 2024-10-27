import csv
import numpy as np
import random

def create_model():
    num_items_1 = 100000
    num_items_2 = 100000
    # Open csv file
    model_csv = open("Test_model.csv", "wt")
    facts_csv = open("Test_facts.csv", "wt")
    header_mod = 'MODEL_TYPE,NODE_TYPE,ID,NAME,PARENT_ID,LEVEL_NUM\n'
    header_fact = 'MODEL_TYPE,NODE_TYPE,FACT_ID,NAME,PARENT_ID,LEVEL_NUM\n'
    # Add header and template
    model_csv.write(header_mod)
    facts_csv.write(header_fact)

    # This script generates private models: 1 and 2.
    # The first model is a private model of a billing system of telecom operator.
    # This model deals with terms of billing: Billing, User, STB, etc.
    # The second model is a private model of a content control system (PPV events catalogue) of telecom operator
    # This model deals with terms of billing: PPV, PPV_Event, etc.
    # Create Billing user nodes

    #Create Billing user nodes
    for i in range(num_items_1):
        body = "Billing,User," + str(i) + ",User_" + str(i) + ",,0\n"
        model_csv.write(body)
        facts_csv.write(body)

    # Create PPV events nodes
    for i in range(num_items_2):
        body = "PPV,PPV_Event," + str(i) + ",Event_" + str(i) + ",,0\n"
        model_csv.write(body)
        facts_csv.write(body)

    # Create Device user nodes
    for i in range(num_items_1):
        body = "User,User," + str(i) + ",User_" + str(i) + ",,0\n"
        model_csv.write(body)
        facts_csv.write(body)

    # Create Device STB nodes
    for i in range(num_items_1):
        body = "User,STB," + str(i + num_items_1) + ",STB_" + str(i + num_items_1) + "," + str(random.randint(0, num_items_1-1)) + ",0\n"
        model_csv.write(body)
        facts_csv.write(body)

    #Close file
    model_csv.close()
    facts_csv.close()

    # Links rules
    link_rules = open("Links_rules-one-level-TEST.csv", "wt")
    header = 'SRC_MODEL,SRC_ID,SRC_NAME,DIST_MODEL,DIST_ID,DIST_NAME,RULE\n'
    link_rules.write(header)
    for i in range(num_items_1):
        for j in range(9):
            p = str(random.randint(0, num_items_2-1))
            body = "User," + str(i) + ",User_" + str(i) + ",PPV," + p + ",Event_" + p + ",entitled\n"
            link_rules.write(body)
    link_rules.close()

    return 1

if __name__ == "__main__":
    create_model()