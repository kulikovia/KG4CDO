import csv
import numpy as np
import time
from datetime import datetime


class base_item:
    def start(self, model_type, node_type, id, name, parent_id, level_num):
        self.model_type = model_type
        self.node_type = node_type
        self.id = id
        self.name = name
        self.parent_id = parent_id
        self.level_num = level_num


def load_facts(facts_path, level_num):
    facts = []
    with open(facts_path) as f_obj:
        reader = csv.DictReader(f_obj, delimiter=',')
        i = 0
        # Open User Requirements file
        for line in reader:
            if level_num == -1:
                facts.append(base_item())
                facts[i].model_type = line["MODEL_TYPE"]
                facts[i].node_type = line["NODE_TYPE"]
                facts[i].id = line["FACT_ID"]
                facts[i].name = line["NAME"]
                facts[i].parent_id = line["PARENT_ID"]
                if facts[i].parent_id == '':
                    facts[i].parent_id = '-1'
                facts[i].level_num = line["LEVEL_NUM"]
                return np.array(facts)
            elif int(line["LEVEL_NUM"] == level_num):
                facts.append(base_item())
                facts[i].model_type = line["MODEL_TYPE"]
                facts[i].node_type = line["NODE_TYPE"]
                facts[i].id = line["FACT_ID"]
                facts[i].name = line["NAME"]
                facts[i].parent_id = line["PARENT_ID"]
                if facts[i].parent_id == '':
                    facts[i].parent_id = '-1'
                facts[i].level_num = line["LEVEL_NUM"]
                i = i + 1

    return np.array(facts)

def load_model(model_req_path, level_num):
    model = []
    with open(model_req_path) as f_obj:
        reader = csv.DictReader(f_obj, delimiter=',')
        i = 0
        # Open User Requirements file
        for line in reader:
            if int(line["LEVEL_NUM"]) == level_num:
                model.append(base_item())
                model[i].model_type = line["MODEL_TYPE"]
                model[i].node_type = line["NODE_TYPE"]
                model[i].id = line["ID_SRC"]
                model[i].name = line["NAME"]
                model[i].parent_id = line["PARENT_ID"]
                if model[i].parent_id == '':
                    model[i].parent_id = '-1'
                model[i].level_num = line["LEVEL_NUM"]
                i = i + 1
    return np.array(model)


def deductive_synthesis(model_req_path, facts_path, max_level):
    print(datetime.now(), " - Deductive synthesis is Started")
    t0 = float(time.time() * 1000)
    # Deductive analysis
    t2 = float(time.time() * 1000)
    # Process the set of facts
    t03 = float(time.time() * 1000)
    for j in range(max_level):
        level_model = load_model(model_req_path, j + 1)
        level_facts = load_facts(facts_path, j + 1)
        main_counter = 0
        for item_1 in level_model:
            for item_2 in level_facts:
                if (item_1.id == item_2.id) and (item_1.model_type == item_2.model_type) and (item_1.node_type == item_2.node_type) and (item_1.name == item_2.name) and (item_1.parent_id == item_2.parent_id) and (item_1.level_num == item_2.level_num):
                    main_counter = main_counter + 1

        if (main_counter == len(level_model)):
            resolution = str("The model is proved. Level number: " + str(j + 1))
            t3 = float(time.time() * 1000)
            print(datetime.now(), ' -', resolution)
            print(datetime.now(), " - Exec. time for Level: " + str(j + 1) + " - " + str(t3 - t2) + "ms.")

            return resolution
        else:
            continue
    resolution = str("The model is not proved.")
    t3 = float(time.time() * 1000)
    print(datetime.now(), ' -', resolution)
    print(datetime.now(), " - Exec. time for Level: " + str(j + 1) + " - " + str(t3 - t2) + "ms.")

    return resolution

def deductive_synthesis_modified(model_req_path, singl_fact_path):
    print(datetime.now(), " - Deductive synthesis is Started")
    t0 = float(time.time() * 1000)
    # Deductive analysis
    t2 = float(time.time() * 1000)
    # Process the set of facts
    t03 = float(time.time() * 1000)
    singl_fact = load_facts(singl_fact_path, -1)
    level_num = singl_fact[0].level_num

    level_model = load_model(model_req_path, level_num)
    main_counter = 0
    for item_1 in level_model:
        if (item_1.id == singl_fact[0].id) and (item_1.model_type == singl_fact[0].model_type) and (item_1.node_type == singl_fact[0].node_type) and (item_1.name == singl_fact[0].name) and (item_1.parent_id == singl_fact[0].parent_id) and (item_1.level_num == singl_fact[0].level_num):
            main_counter = main_counter + 1

    resolution = str("The fact is processed.")
    t3 = float(time.time() * 1000)
    print(datetime.now(), ' -', resolution)
    print(datetime.now(), " - Exec. time for Level: " + str(level_num) + " - " + str(t3 - t2) + "ms.")

    return resolution






if __name__ == "__main__":
    #resolution = deductive_synthesis('Req.csv', 'TMP/Test_facts1.csv', 5)

    #resolution = deductive_synthesis_modified('Req.csv', 'TMP/Test_facts1.csv')