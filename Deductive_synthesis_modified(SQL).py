import csv
import numpy as np
import time
from datetime import datetime, date
import psycopg2

#Level number for deductive synthesis

level_num = 0

#Open DB connection
con = psycopg2.connect(
   database="Synthesis_mod_AI",
   user="postgres",
   password="admin",
   host="127.0.0.1",
   port="5433"
    )
#Clear DB tables
cur = con.cursor()
cur.execute('''TRUNCATE TABLE public."Facts";''')
cur.execute('''TRUNCATE TABLE public."Req_model";''')
cur.execute('''TRUNCATE TABLE public."Facts_processed";''')
con.commit()


class src_node:

    def start(self, model_type, node_type, id, name, parent_id):
        self.model_type = model_type
        self.node_type = node_type
        self.id = id
        self.name = name
        self.parent_id = parent_id

class src_model:

    def start(self, file_name, model1):
        model = []
        with open(file_name) as f_obj:
            csv_dict_reader_models(f_obj, model)
        self.model1 = model

class req_model:

    def start(self, file_name, model1):
        model = []
        with open(file_name) as f_obj:
            csv_dict_reader_models(f_obj, model)
        self.model1 = model

class facts_model:

    def start(self, file_name, model1):
        model = []
        with open(file_name) as f_obj:
            csv_dict_reader_facts_and_req_model(f_obj, model)
        self.model1 = model

class base_node:

    def start(self, base_id, model_type, node_type, id, name, parent_id, level_num):
        self.base_id = base_id
        self.model_type = model_type
        self.node_type = node_type
        self.id = id
        self.name = name
        self.parent_id = parent_id
        self.base_parent_id = base_parent_id
        self.level_num = level_num

class base_link:
    def start(self, id, src_link, dist_link, rule, notes):
        self.id = id
        self.src_link = src_link
        self.dist_link = dist_link
        self.rule = rule
        self.notes = notes

class base_rules:
    def start(self, src_node_type, dist_node_type, rule):
        self.src_node_type = src_node_type
        self.dist_node_type = dist_node_type
        self.rule = rule

class base_requirements:
    def start(self, model_type, node_type, id, name):
        self.model_type = model_type
        self.node_type = node_type
        self.id = id
        self.name = name
        self.base_id = base_id

class base_model:
    def start(self):
        self.model = []
        self.model_req = []
        self.links = []
        self.links_req = []
        self.requirements = []

class goal:

    def start(self, goal_id, goal_desc, level_num, node_id, goal_state):
        self.goal_id = goal_id
        self.goal_desc = goal_desc
        self.level_num = level_num
        self.node_id = node_id
        self.goal_state = goal_state

class fact:

    def start(self, fact_state, model_type, node_type, id, name, parent_id):
        self.fact_state = fact_state
        self.model_type = model_type
        self.node_type = node_type
        self.id = id
        self.name = name
        self.parent_id = parent_id

def csv_dict_reader_models(file_obj, model):
    """
    Read a CSV file using csv.DictReader
    """
    reader = csv.DictReader(file_obj, delimiter=',')
    i=0
    for line in reader:
        model.append(src_node())
        model[i].model_type = line["MODEL_TYPE"]
        model[i].node_type = line["NODE_TYPE"]
        model[i].id = line["ID"]
        model[i].name = line["NAME"]
        model[i].parent_id = line["PARENT_ID"]
        i = i+1
    return model

def csv_dict_reader_facts_and_req_model(file_obj_rules, model):
    """
    Read a CSV file using csv.DictReader
    """
    reader = csv.DictReader(file_obj_rules, delimiter=',')

    i=0
    for line in reader:
        model.append(fact())
        model[i].model_type = line["MODEL_TYPE"]
        model[i].node_type = line["NODE_TYPE"]
        model[i].id = line["FACT_ID"]
        model[i].name = line["NAME"]
        model[i].parent_id = line["PARENT_ID"]
        model[i].level_num = line["LEVEL_NUM"]
        i = i+1
    t0 = float(time.time() * 1000)
    #Set of facts importing
    #sql = '''COPY "Facts" ("MODEL_TYPE", "NODE_TYPE", "FACT_ID", "NAME", "PARENT_ID", "LEVEL_NUM") FROM 'C:\Blazegraph\Projects\Test_facts1.csv' WITH DELIMITER ',' CSV HEADER;'''
    # Single fact importing
    sql = '''COPY "Facts" ("MODEL_TYPE", "NODE_TYPE", "FACT_ID", "NAME", "PARENT_ID", "LEVEL_NUM") FROM 'C:\Blazegraph\Projects\Test_one_facts1.csv' WITH DELIMITER ',' CSV HEADER;'''
    cur.execute(sql)
    con.commit()
    print(datetime.now(), " - Set of facts has been imported")
    t1 = float(time.time() * 1000)
    print(datetime.now(), " - Facts import time: " + str(t1 - t0) + "ms.")
    t02 = float(time.time() * 1000)
    sql = '''COPY "Req_model" ("ID", "MODEL_TYPE", "NODE_TYPE", "SRC_ID", "NAME", "PARENT_ID", "LEVEL_NUM") FROM 'C:\Blazegraph\Projects\Req_model_1.csv' WITH DELIMITER ',' CSV HEADER;'''
    cur.execute(sql)
    con.commit()
    print(datetime.now(), ' - The rules readed')
    t12 = float(time.time() * 1000)
    print(datetime.now(), " - Rules reading time: " + str(t12 - t02) + "ms.")
    #Process the set of facts
    t03 = float(time.time() * 1000)
    sql = '''INSERT INTO public."Facts_processed" ("FACT_ID", "LEVEL_NUM","isAchieved","CONTROL_DATE")
                    SELECT d."FACT_ID", s."LEVEL_NUM", 1, current_timestamp FROM public."Req_model" as s JOIN public."Facts" as d 
                        ON s."MODEL_TYPE" = d."MODEL_TYPE" 
                        AND s."NODE_TYPE" = d."NODE_TYPE"
                        AND s."NAME" = d."NAME"
                        AND s."SRC_ID" = d."FACT_ID"
                        WHERE s."LEVEL_NUM" = ''' + str(level_num) + ''';'''
    cur.execute(sql)
    con.commit()
    print(datetime.now(), ' - The current factes have been processed')
    t13 = float(time.time() * 1000)
    print(datetime.now(), " - Facts processing time: " + str(t13 - t03) + "ms.")
    return model

def deductive_synthesis(model, facts, level_num):
    num = 0
    max_level = 0
    for i in range(len(model)):
        if max_level < int(model[i].level_num):
            max_level = int(model[i].level_num)
    print(datetime.now(), ' - The model Max_level= ', max_level)

    sql = '''SELECT count(s."isAchieved") FROM public."Facts_processed" as s
                WHERE "LEVEL_NUM" = ''' + str(level_num) + '''AND "isAchieved" = 1;'''

    cur.execute(sql)
    con.commit()
    level_elements_fact_achieved = cur.fetchall()
    for row in level_elements_fact_achieved:
        level_elements_fact_achieved_int = row[0]
    sql = '''SELECT count(s."LEVEL_NUM") FROM public."Req_model" as s 
                    WHERE s."LEVEL_NUM" = ''' + str(level_num) + ''';'''
    cur.execute(sql)
    level_elements_req = cur.fetchall()

    if (level_elements_req == level_elements_fact_achieved):
        resolution = str("The model is proved. Complexity: " + str(num) + " Level number: " + str(level_num) + " Len model:" + str (len(model)))
    else:
        resolution = str("The model is not proved. Complexity: " +str(num) + " Elements/Len model:" + str(level_elements_fact_achieved_int) + " / " + str (len(model)))
    return resolution

if __name__ == "__main__":
    print(datetime.now(), " - Deductive synthesis is Started")
    #Import base model from file
    base_obj = base_model()
    file_obj  = np.load('Model_base_req.npz', allow_pickle=True)
    base_obj.model = file_obj['arr_0']
    print(datetime.now(), " - Reference model has been imported")
    t0 = float(time.time() * 1000)
    # Read facts
    facts = facts_model()
    #Positive scenario - the One fact
    facts.start('Test_one_facts1.csv', model1=[])
    #Positive scenario
    #facts.start('Test_facts1.csv', model1=[])
    #Wrong nodes scenario
    #facts.start('Deductive_facts_(wrong_nodes)_1.csv', model1=[])
    # Empty nodes scenario
    #facts.start('Deductive_facts_(empty_nodes)_1.csv', model1=[])
    #Deductive analysis
    t2 = float(time.time() * 1000)
    resolution = deductive_synthesis(base_obj.model, facts.model1,level_num)
    t3 = float(time.time() * 1000)
    print(datetime.now(), ' -', resolution)
    print(datetime.now(), " - Exec. time for Level: " + str(level_num) + " - " + str(t3-t2) + "ms.")
    con.close()





