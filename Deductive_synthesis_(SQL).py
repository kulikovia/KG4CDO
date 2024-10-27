import csv
import numpy as np
import time
from datetime import datetime, date
import psycopg2

#Open DB connection
con = psycopg2.connect(
   database="Synthesis_mod_AI",
   user="postgres",
   password="admin",
   host="127.0.0.1",
   port="5432"
    )

#Set up working directory
work_dir = "C:\\1\\"

#Clear DB tables
cur = con.cursor()
cur.execute('''TRUNCATE TABLE public."Facts";''')
cur.execute('''TRUNCATE TABLE public."Req_model";''')
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
            csv_dict_reader_facts(f_obj, model)
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

def csv_dict_reader_facts(file_obj_rules, model):
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
    sql = '''COPY "Facts" ("MODEL_TYPE", "NODE_TYPE", "FACT_ID", "NAME", "PARENT_ID", "LEVEL_NUM") FROM \'''' + work_dir + 'Test_facts.csv' + '''\' WITH DELIMITER ',' CSV HEADER;'''
    cur.execute(sql)
    con.commit()
    return model

def deductive_synthesis(model, facts):
    sql = '''COPY "Req_model" ("ID", "MODEL_TYPE", "NODE_TYPE", "SRC_ID", "NAME", "PARENT_ID", "LEVEL_NUM") FROM \'''' + work_dir + 'Req_model_1.csv' + '''\' WITH DELIMITER ',' CSV HEADER;'''
    cur.execute(sql)
    con.commit()
    print(datetime.now(), ' - The rules readed')
    num = 0
    goals = []
    test = []
    max_level = 0
    print(datetime.now(), ' - The rules applied')
    print(datetime.now(), ' - The rules red')
    print(datetime.now(), ' - The deductive model proving started')
    for i in range(len(model)):
        if max_level < int(model[i].level_num):
            max_level = int(model[i].level_num)
    print(datetime.now(), ' - The model Max_level= ', max_level)
    k = 0
    i = 0
    l = 0
    while l <= max_level:
        sql = '''SELECT s."ID", s."LEVEL_NUM", s."MODEL_TYPE", s."NODE_TYPE", s."SRC_ID" FROM public."Req_model" as s JOIN public."Facts" as d 
                    ON s."MODEL_TYPE" = d."MODEL_TYPE" 
                    AND s."NODE_TYPE" = d."NODE_TYPE"
                    AND s."NAME" = d."NAME"
                    AND s."SRC_ID" = d."FACT_ID"
                    WHERE s."LEVEL_NUM" = ''' + str(l) +''';'''
        cur.execute(sql)
        con.commit()
        rows = cur.fetchall()
        #print(sql)
        for row in rows:
            goals.append(goal())
            goals[k].goal_id = row[0]
            goals[k].goal_desc = "Goal achieved."
            goals[k].level_num = row[1]
            goals[k].node_id = row[4]
            test.append(str(datetime.now()) + " - Goal achieved. Goal ID: " + str(goals[k].goal_id) + " Level num: " + str(
                goals[k].level_num) + " Node ID: " + str(goals[k].node_id))
            #print(test[k])
            k = k + 1
            i = i + 1
            num = num + 1

        #Check level l logic (if target model proved)
        sql = '''SELECT count(s."LEVEL_NUM") FROM public."Req_model" as s JOIN public."Facts" as d 
                    ON s."MODEL_TYPE" = d."MODEL_TYPE" 
                    AND s."NODE_TYPE" = d."NODE_TYPE"
                    AND s."NAME" = d."NAME"
                    AND s."SRC_ID" = d."FACT_ID"
                    WHERE s."LEVEL_NUM" = ''' + str(l) + ''';'''
        cur.execute(sql)
        level_elements_fact = cur.fetchall()
        sql = '''SELECT count(s."LEVEL_NUM") FROM public."Req_model" as s 
                    WHERE s."LEVEL_NUM" = ''' + str(l) + ''';'''
        cur.execute(sql)
        level_elements_req = cur.fetchall()
        if (level_elements_req == level_elements_fact) and (num > 0):
            resolution = str("The model is proved. Complexity: " + str(num) + " Level number: " + str(l) + " Len model:" + str (len(model)))
            return resolution
        l = l + 1
    n = 0
    for p in range(len(goals)):
        if (goals[p].goal_desc == "Goal achieved."):
            n = n + 1
            num = num + 1
    if n == len(model):
        resolution = str("The model is proved. Complexity: " + str(num) + " Elements/Len model:" + str(n) + " / " + str (len(model)))
    else:
        resolution = str("The model is not proved. Complexity: " +str(num) + " Elements/Len model:" + str(n) + " / " + str (len(model)))

    return resolution

if __name__ == "__main__":
    print(datetime.now(), " - Deductive synthesis is Started")
    t0 = int(time.time() * 1000)
    #Import base model from file
    base_obj = base_model()
    file_obj  = np.load(work_dir + 'Model_base_req.npz', allow_pickle=True)
    base_obj.model = file_obj['arr_0']
    print(datetime.now(), " - Reference model has been imported")
    # Read facts
    facts = facts_model()
    #Positive scenario
    facts.start(work_dir + 'Test_facts.csv', model1=[])
    #Wrong nodes scenario
    #facts.start('Deductive_facts_(wrong_nodes)_1.csv', model1=[])
    # Empty nodes scenario
    #facts.start('Deductive_facts_(empty_nodes)_1.csv', model1=[])
    print(datetime.now(), " - Set of facts has been imported")
    #Deductive analysis
    t1 = int(time.time() * 1000)
    resolution = deductive_synthesis(base_obj.model, facts.model1)
    t2 = int(time.time() * 1000)
    print(datetime.now(), ' -', resolution)
    print(datetime.now(), " - Exec. time: " + str(t2-t1) + "ms.")
    con.close()





