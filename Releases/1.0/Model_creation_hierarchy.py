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
    #Open and read template
    template = open("Test_template_1.csv", "r")
    body = template.read()
    # Add header and template
    model_csv.write(header_mod)
    facts_csv.write(header_fact)
    model_csv.write(body)
    facts_csv.write(body)

    template.close()

    #This script generates private models: 1 and 2.
    # The first model is a private model of a billing system of telecom operator.
    # This model deals with terms of billing: Billing, User, STB, etc.
    #The second model is a private model of a content control system (PPV events catalogue) of telecom operator
    # This model deals with terms of billing: PPV, PPV_Event, etc.
    #Create Billing user nodes
    for i in range(num_items_1):
        body = "Billing,User," + str(i + 12) + ",User_" + str(i + 12) + "," + str(random.randint(2, 6)) + ":" + str(random.randint(7, 11)) + ",2\n"
        model_csv.write(body)
        facts_csv.write(body)

    # Create PPV events nodes
    for i in range(num_items_2):
        body = "PPV,PPV_Event," + str(i + 19) + ",Event_" + str(i + 19) + "," + str(random.randint(9, 18)) + ",3\n"
        model_csv.write(body)
        facts_csv.write(body)

    # Create Device user nodes
    for i in range(num_items_1):
        body = "User,User," + str(i + 12) + ",User_" + str(i + 12) + "," + str(random.randint(2, 6)) + ",2\n"
        model_csv.write(body)
        facts_csv.write(body)

    # Create Device STB nodes
    for i in range(num_items_1):
        body = "User,STB," + str(i + 13 + num_items_1) + ",STB_" + str(i + 13 + num_items_1) + "," + str(random.randint(12, 11 + num_items_1)) + ",3\n"
        model_csv.write(body)
        facts_csv.write(body)

    #Close file
    model_csv.close()
    facts_csv.close()
    return 1

if __name__ == "__main__":
    create_model()