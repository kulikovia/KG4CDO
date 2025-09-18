import csv
import numpy as np
import psycopg2
import random
from random import randrange
from datetime import datetime
from datetime import timedelta
import time

def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

d1 = datetime.strptime('7/25/20 00:00:00', '%m/%d/%y %H:%M:%S')
d2 = datetime.strptime('7/26/20 23:59:59', '%m/%d/%y %H:%M:%S')


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

#Set up model type
model_type = 1 #1 - hierarchical model; 0 - one-level model

#Clear DB tables
print("Connected to DB")
cur = con.cursor()
cur.execute('''TRUNCATE TABLE public."Base_model";''')
con.commit()
print("Table Base_model truncated")
cur.execute('''TRUNCATE TABLE public."Req_model";''')
con.commit()
print("Table Req_model truncated")
cur.execute('''TRUNCATE TABLE public."Base_links";''')
con.commit()
print("Table Base_links truncated")
cur.execute('''TRUNCATE TABLE public."Req";''')
con.commit()
print("Req truncated")
cur.execute('''TRUNCATE TABLE public."Req_links";''')
con.commit()
print("Table Req_links truncated")
cur.execute('''TRUNCATE TABLE public."Temp_table";''')
con.commit()
print("Temp_table truncated")
cur.execute('''TRUNCATE TABLE public."Temp_table2";''')
con.commit()
print("Temp_table2 truncated")


class src_node:

    def start(self, model_type, node_type, id, name, parent_id, level_num):
        self.model_type = model_type
        self.node_type = node_type
        self.id = id
        self.name = name
        self.parent_id = parent_id
        self.level_num = level_num

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
            self.model1 = csv_dict_reader_requirements(f_obj)


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
    def start(self, id, src_link, dist_link, src_name, dist_name, rule, notes):
        self.id = id
        self.src_link = src_link
        self.dist_link = dist_link
        self.src_name = src_name
        self.dist_name = dist_name
        self.rule = rule
        self.notes = notes

class base_rules:
    def start(self, src_model, src_id, src_name, dist_model, dist_id, dist_name, rule):
        self.src_model = src_model
        self.src_id = src_id
        self.src_name = src_name
        self.dist_model = dist_model
        self.dist_id = dist_id
        self.dist_name = dist_name
        self.rule = rule

class base_requirements:
    def start(self, model_type, node_type, id, name, parent_id, level_num):
        self.model_type = model_type
        self.node_type = node_type
        self.id = id
        self.name = name
        self.parent_id = parent_id
        self.level_num = level_num

class base_model:
    def start(self):
        self.model = []
        self.model_req = []
        self.links = []
        self.links_req = []
        self.requirements = []
        self.index = []
        self.index_req = []

    def add_model(self, src_model):
        # Open SPARQL file
        csv_f = open(work_dir + 'Base.csv', "wt")
        j = len(self.model)
        for i in range(len(src_model.model1)):
            self.model.append(base_node())
            self.model[j].base_id = '-1'
            self.model[j].model_type = src_model.model1[i].model_type
            self.model[j].node_type = src_model.model1[i].node_type
            self.model[j].id = src_model.model1[i].id
            self.model[j].name = src_model.model1[i].name
            self.model[j].parent_id = src_model.model1[i].parent_id
            self.model[j].base_parent_id = ''
            self.model[j].level_num = src_model.model1[i].level_num
            self.index.append(str)
            self.index[j] = src_model.model1[i].model_type + ":" + str(src_model.model1[i].id)
            if self.model[j].parent_id == "":
                self.model[j].parent_id = '-1'
            line = str(j) + ',' + self.model[j].model_type + ',' + self.model[j].node_type + ',' + self.model[j].name + ',' + str(self.model[j].id) + ',' + self.model[j].parent_id + ',' + self.model[j].level_num + '\n'
            csv_f.write(line)
            j = j + 1
        csv_f.close()
        sql = '''COPY "Base_model" ("ID", "MODEL_TYPE", "NODE_TYPE", "NAME", "SRC_ID", "PARENT_ID", "LEVEL_NUM") FROM \'''' + work_dir + 'Base.csv' + '''\' WITH DELIMITER ',' ;'''
        cur.execute(sql)
        con.commit()


    def id_normalisation(self):
        for i in range(len(self.model)):
            self.model[i].base_id = self.model[i].model_type + '-' + self.model[i].id
            parent_str = self.model[i].parent_id
            parent_set = parent_str.split(":")
            parent_str = ''
            if len(parent_set) > 1:
                for p in range(len(parent_set)):
                    parent_set[p] = self.model[i].model_type + '-' + parent_set[p]
                    parent_str = ':'.join(parent_set)
                self.model[i].base_parent_id = parent_str
            else:
                if parent_set[0] == '':
                    self.model[i].base_parent_id = ''
                else:
                    self.model[i].base_parent_id = self.model[i].model_type + '-' + parent_set[0]
        return 1

    def create_base_links(self, rules_file):
        j=0
        for i in range(len(self.model)):
            if self.model[i].base_parent_id != '':
                parent_str = str(self.model[i].base_parent_id)
                parent_set = parent_str.split(":")
                for p in range(len(parent_set)):
                    self.links.append(base_link())
                    self.links[j].start(j ,parent_set[p], self.model[i].base_id, '',self.model[i].name, 'includes', 0)
                    j = j+1

        with open(rules_file) as f_obj:
            self.rules = csv_dict_reader_rules(f_obj)

        for n in range(len(self.rules)):
            self.links.append(base_link())
            self.links[j].id = j
            self.links[j].src_link = self.rules[n].src_model + '-' + self.rules[n].src_id
            self.links[j].dist_link = self.rules[n].dist_model + '-' + self.rules[n].dist_id
            self.links[j].src_name = self.rules[n].src_name
            self.links[j].dist_name = self.rules[n].dist_name
            self.links[j].rule = self.rules[n].rule
            j = j + 1


    def use_requirements(self, req_obj):
        # Rejecting nodes from the base model
        sql = '''Copy (SELECT s."ID", s."MODEL_TYPE", s."NODE_TYPE", s."SRC_ID", s."NAME", s."PARENT_ID", s."LEVEL_NUM" FROM public."Base_model" as s JOIN public."Req" as d ON s."MODEL_TYPE" = d."MODEL_TYPE" AND s."NODE_TYPE" = d."NODE_TYPE" AND s."SRC_ID" = d."SRC_ID" AND s."PARENT_ID" = d."PARENT_ID" AND s."NAME" = d."NAME") To \'''' + work_dir + 'Req_model_1.csv' + '''\' With CSV DELIMITER ',' HEADER;'''
        cur.execute(sql)
        con.commit()
        print('Req object: The JOIN #1 executed')
        l = 0
        with open(work_dir + 'Req_model_1.csv') as f_obj:
            reader = csv.DictReader(f_obj, delimiter=',')
            for line in reader:
                self.model_req.append(base_node())
                self.model_req[l].base_id = -1
                self.model_req[l].base_parent_id = ''
                self.model_req[l].model_type = line["MODEL_TYPE"]
                self.model_req[l].node_type = line["NODE_TYPE"]
                self.model_req[l].name = line["NAME"]
                self.model_req[l].id = line["SRC_ID"]
                self.model_req[l].parent_id = line["PARENT_ID"]
                self.model_req[l].level_num = line["LEVEL_NUM"]
                l = l + 1
            print('Part#1 finnished')
            con.close()
        #Base ID set / ID normalisation
        print('ID normalisation started')
        for i in range(len(self.model_req)):
            self.model_req[i].base_id = self.model_req[i].model_type + '-' + self.model_req[i].id
            parent_str = self.model_req[i].parent_id
            parent_set = parent_str.split(":")
            parent_str = ''
            if len(parent_set) > 1:
                for p in range(len(parent_set)):
                    parent_set[p] = self.model_req[i].model_type + '-' + parent_set[p]
                    parent_str = ':'.join(parent_set)
                self.model_req[i].base_parent_id = parent_str
            else:
                if parent_set[0] == '':
                    self.model_req[i].base_parent_id = ''
                else:
                    self.model_req[i].base_parent_id = self.model_req[i].model_type + '-' + parent_set[0]
        return 1

    def create_req_base_links(self, rules_file):
        j = 0
        for i in range(len(self.model_req)):
            if self.model_req[i].base_parent_id != '':
                parent_str = str(self.model_req[i].base_parent_id)
                parent_set = parent_str.split(":")
                for p in range(len(parent_set)):
                    self.links_req.append(base_link())
                    self.links_req[j].start(j, parent_set[p], self.model_req[i].base_id, '', self.model_req[i].name, 'includes', 0)
                    j = j + 1

        with open(rules_file) as f_obj:
            self.rules = csv_dict_reader_rules(f_obj)

        for n in range(len(self.rules)):
            self.links_req.append(base_link())
            self.links_req[j].id = j
            self.links_req[j].src_link = self.rules[n].src_model + '-' + self.rules[n].src_id
            self.links_req[j].dist_link = self.rules[n].dist_model + '-' + self.rules[n].dist_id
            self.links_req[j].src_name = self.rules[n].src_name
            self.links_req[j].dist_name = self.rules[n].dist_name
            self.links_req[j].rule = self.rules[n].rule
            j = j + 1

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
        model[i].level_num = line["LEVEL_NUM"]
        i = i+1
    return model

def csv_dict_reader_rules(file_obj_rules):
    """
    Read a CSV file using csv.DictReader
    """
    rules = []
    reader = csv.DictReader(file_obj_rules, delimiter=',')

    i=0
    for line in reader:
        rules.append(base_rules())
        rules[i].src_model = line["SRC_MODEL"]
        rules[i].src_id = line["SRC_ID"]
        rules[i].src_name = line["SRC_NAME"]
        rules[i].dist_model = line["DIST_MODEL"]
        rules[i].dist_id = line["DIST_ID"]
        rules[i].dist_name = line["DIST_NAME"]
        rules[i].rule = line["RULE"]
        i = i+1
    return rules

def csv_dict_reader_requirements(file_obj_rules):
    """
    Read a CSV file using csv.DictReader
    """
    requirements = []
    reader = csv.DictReader(file_obj_rules, delimiter=',')
    print("Req dic entered")
    i=0
    # Open CSV file
    csv_f = open(work_dir + 'Req.csv', "wt")
    for line in reader:
        requirements.append(base_requirements())
        requirements[i].model_type = line["MODEL_TYPE"]
        requirements[i].node_type = line["NODE_TYPE"]
        requirements[i].id = line["ID"]
        requirements[i].name = line["NAME"]
        requirements[i].parent_id = line["PARENT_ID"]
        if requirements[i].parent_id == '':
            requirements[i].parent_id = '-1'
        requirements[i].level_num = line["LEVEL_NUM"]
        line = str(i) + ',' + requirements[i].model_type + ',' + requirements[i].node_type + ',' + requirements[i].name + ',' + str(requirements[i].id)+ ',' + requirements[i].parent_id + ',' + requirements[i].level_num + '\n'
        csv_f.write(line)
        i = i + 1
    csv_f.close()
    sql = '''COPY "Req" ("ID", "MODEL_TYPE", "NODE_TYPE", "NAME", "SRC_ID", "PARENT_ID", "LEVEL_NUM") FROM \'''' + work_dir + 'Req.csv' + '''\' WITH DELIMITER ',' ;'''
    cur.execute(sql)
    con.commit()
    return requirements

def create_rdf_model(model, links, file_name):
    genres = ['Sport', 'Comedy', 'Documentary', 'Geography']
    # Open file
    spql = open(file_name, "wt")
    # Add header
    header = str(
        "<?xml version='1.0' encoding='UTF-8'?>\n<rdf:RDF\nxmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'\nxmlns:vCard='http://www.w3.org/2001/vcard-rdf/3.0#'\nxmlns:my='http://127.0.0.1/bg/ont/test1#'\n>")

    spql.write(header)

    #Create nodes
    for i in range(len(model)):
        body = str("\n<rdf:Description rdf:about='http://127.0.0.1/") + str(model[i].name) + str("/'>\n<my:has_id>") + str(model[i].base_id) + str("</my:has_id>\n <my:has_type>") + str(model[i].node_type) + str("</my:has_type>\n")
        if model[i].node_type == 'PPV_Event':
            body = body + str("<my:has_genre>") + str(random.choice(genres)) + str("</my:has_genre>\n")
        body = body + str("<my:has_description>") + str("Model type: ") + str(model[i].model_type) + str(", Node type: ") + str(model[i].node_type) + str(", Node name: ") + str(model[i].name)+ str("</my:has_description>\n</rdf:Description>\n")
        spql.write(body)

    #Create links
    for i in range(len(links)):
        body = str("\n<rdf:Description rdf:about='http://127.0.0.1/Link_") + str(i) + str("/'>\n<my:src_node_id>") + str(links[i].src_link) + str("</my:src_node_id>\n<my:dist_node_id>") + str(links[i].dist_link) + str("</my:dist_node_id>\n<my:used_rule>") + str(links[i].rule)+ str("</my:used_rule>\n</rdf:Description>\n")
        spql.write(body)

    spql.close()
    return 1

def create_dynamic_data(file_name, num):
    # Open SPARQL file
    spql = open(file_name, "a")
    # Add header
    header = str(
        "<?xml version='1.0' encoding='UTF-8'?>\n<rdf:RDF\nxmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'\nxmlns:vCard='http://www.w3.org/2001/vcard-rdf/3.0#'\nxmlns:my='http://127.0.0.1/bg/ont/test1#'\n>")

    #spql.write(header)

    #Create entries
    reg = ['https://sws.geonames.org/8504951/', 'https://sws.geonames.org/510291/',
           'https://sws.geonames.org/546105/', 'https://sws.geonames.org/8504949/',
           'https://sws.geonames.org/8504953/']

    spql.write("\n<!--User action definitions PPV purchases-->\n")

    for i in range(num):
        body = str("<rdf:Description rdf:about='http://127.0.0.1/Request_A") + str(i) + str(
                "/'><my:request_timestamp rdf:datatype='http://www.w3.org/2001/XMLSchema#datetime'>") + str(
                random_date(d1, d2).strftime("%Y-%m-%dT%H:%M:%S")) + str(
                "</my:request_timestamp>\n<my:request_geodata><rdf:Description rdf:about='") + str(
                random.choice(reg)) + str("'></rdf:Description></my:request_geodata>\n<my:has_req_type>PPV_purchased</my:has_req_type>\n<my:request_detailes>\n<rdf:Description>\n<rdf:type>:statement</rdf:type>\n<rdf:predicat>:ppv_purchase</rdf:predicat>\n<rdf:subject><rdf:Description rdf:about='http://127.0.0.1/Event_") + str(random.randint(19, 99)) + str("/'></rdf:Description></rdf:subject>\n<rdf:object>\n<rdf:Description rdf:about='http://127.0.0.1/User_") + str(
                random.randint(12, 11 + num)) + str("/'></rdf:Description></rdf:object>\n</rdf:Description>\n</my:request_detailes>\n</rdf:Description>\n")
        spql.write(body)

    #Create footer
    spql.write("\n</rdf:RDF>\n")
    spql.close()
    return 1


if __name__ == "__main__":
    t0 = int(time.time() * 1000)
    tn = t0
    print("Started")
    #Import src model
    src_obj = src_model()
    src_obj.start("Test_model.csv", model1 = [])
    t1 = int(time.time() * 1000)
    print("SRC model imported. Time: " + str(t1-t0) + " ms.")
    # Create base model
    base_obj = base_model()
    base_obj.start()
    t0 = t1
    t1 = int(time.time() * 1000)
    print("Base model created. Time: " + str(t1-t0) + " ms.")
    # Add src model
    base_obj.add_model(src_obj)
    t0 = t1
    t1 = int(time.time() * 1000)
    print("SRC model added. Time: " + str(t1-t0) + " ms.")
    # ID normalisation
    base_obj.id_normalisation()
    t0 = t1
    t1 = int(time.time() * 1000)
    print("Indexes normalized. Time: " + str(t1-t0) + " ms.")
    if model_type == 1:
        # Base links creation - hierarchical
        base_obj.create_base_links('Links_rules.csv')
    else:
        # Base links creation - one-level
        base_obj.create_base_links('Links_rules-one-level-TEST.csv')
    t0 = t1
    t1 = int(time.time() * 1000)
    print("Base links created. Time: " + str(t1-t0) + " ms.")
    # Create requirements object
    req_obj = req_model()
    req_obj.start("Test_model.csv", model1=[])
    t0 = t1
    t1 = int(time.time() * 1000)
    print("Req object created. Time: " + str(t1-t0) + " ms.")
    # Using requirements
    base_obj.use_requirements(req_obj)
    t0 = t1
    t1 = int(time.time() * 1000)
    print("Reqs applyed. Time: " + str(t1-t0) + " ms.")
    if model_type == 1:
        # Create links for model_req - hierarchical
        base_obj.create_req_base_links('Links_rules.csv')
    else:
        # Create links for model_req - one-level
        base_obj.create_req_base_links('Links_rules-one-level-TEST.csv')
    t0 = t1
    t1 = int(time.time() * 1000)
    print("Req model links created. Time: " + str(t1-t0) + " ms.")
    #Create base RDF model
    create_rdf_model(base_obj.model, base_obj.links, work_dir + 'Base_rdf_1.xml')
    #Create user req. RDF model
    create_rdf_model(base_obj.model_req, base_obj.links_req, work_dir + 'Req_rdf_1.xml')
    # Create dynamic data
    create_dynamic_data(work_dir + 'Req_rdf_1.xml', 100)
    # Saving models to files
    np.savez(work_dir + 'Model_base', base_obj.model, allow_pickle=True)
    np.savez(work_dir + 'Model_base_links', base_obj.links, allow_pickle=True)
    np.savez(work_dir + 'Model_base_req', base_obj.model_req, allow_pickle=True)
    np.savez(work_dir + 'Model_base_links_req', base_obj.links_req, allow_pickle=True)
    t0 = t1
    t1 = int(time.time() * 1000)
    print("Models saved. Time: " + str(t1-t0) + " ms.")
    print("Total time spent: " + str(t1 - tn) + " ms.")
    con.close()