import csv
import numpy as np
import time

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
    def start(self, file_name, model1, base_obj):
        model = []
        with open(file_name) as f_obj:
            self.model1 = csv_dict_reader_requirements(f_obj, base_obj)

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
        csv_f = open('Base.csv', "wt")
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


    def use_requirements(self):
        #Insert Requirements to req_model if node is existed in the model
        for item_1 in self.requirements:
            for item_2 in self.model:
                if (item_1.id == item_2.id) and (item_1.model_type == item_2.model_type) and (item_1.node_type == item_2.node_type) and (item_1.name == item_2.name) and (item_1.parent_id == item_2.parent_id) and (item_1.level_num == item_2.level_num):
                    self.model_req.append(item_2)
        return 1

    def create_req_base_links(self, rules_file):
        with open(rules_file) as f_obj:
            self.rules = csv_dict_reader_rules(f_obj)
        j = 0
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
        model[i].model_type = line["MODEL_TYPE"]    #0
        model[i].node_type = line["NODE_TYPE"]      #1
        model[i].id = line["ID"]                    #2
        model[i].name = line["NAME"]                #3
        model[i].parent_id = line["PARENT_ID"]      #4
        model[i].level_num = line["LEVEL_NUM"]      #5
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

def csv_dict_reader_requirements(file_obj_rules, base_obj):
    """
    Read a CSV file using csv.DictReader
    """
    requirements = []
    reader = csv.DictReader(file_obj_rules, delimiter=',')
    print("Req dic entered")
    i=0
    # Open User Requirements file
    csv_f = open('Req.csv', "wt")
    header_mod = 'ID,MODEL_TYPE,NODE_TYPE,NAME,ID_SRC,PARENT_ID,LEVEL_NUM\n'
    csv_f.write(header_mod)
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
    base_obj.requirements = requirements
    return requirements


def rdf_xml_creation(base_obj, Model_path, SPARQL_path, IRI_prefix):
    filename = 'data'
    Max_Step_1 = 100000

    # Open SPARQL file
    spql = open(Model_path + "sparql_script.spql", "wt")

    # Add header
    header = str(
        "<?xml version='1.0' encoding='UTF-8'?>\n<rdf:RDF\nxmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'\nxmlns:vCard='http://www.w3.org/2001/vcard-rdf/3.0#'\nxmlns:test_ont='http://127.0.0.1/ont/test1#'\n>")

    # Models core definition
    # Model i hierarchy definition
    FileNum = 0
    i = 1
    while i < len(base_obj.model_req):
        k = 1
        FileNum = FileNum + 1
        model_type = base_obj.model_req[i].model_type
        level_num = base_obj.model_req[i].level_num
        f = open(
            Model_path + filename + str(model_type) + "_level" + str(level_num) + "_" + str(FileNum) + "_.rdf",
            "at")
        f.write(header)
        f.write("\n<!--Objects definitions-->\n")
        while k <= Max_Step_1:
            body = "<rdf:Description rdf:about='" + IRI_prefix + str(base_obj.model_req[i].name) + "/'>\n<test_ont:has_id>Core_" + str(base_obj.model_req[i].model_type) + "_element_" + str(base_obj.model_req[i].id) + "</test_ont:has_id>\n<test_ont:has_parent_id><rdf:Description rdf:about='" + IRI_prefix + "/Core_" + str(base_obj.model_req[i].model_type) + "_element_" + str(base_obj.model_req[i].parent_id) + "/' /></test_ont:has_parent_id>\n</rdf:Description>\n\n"

            f.write(body)
            i = i + 1
            if i >= len(base_obj.model_req):
                break
            k = k + 1
        f.write("\n</rdf:RDF>\n")
        f.close()
        spql.write(
            "\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + str(model_type) + "_level" + str(level_num) + "_" + str(FileNum) + "_.rdf>;\n")
        k = 1

    FileNum = 0
    i = 1
    while i < len(base_obj.links_req):
        f = open(Model_path + filename + "_links_" + str(FileNum) + "_.rdf", "at")
        f.write(header)
        f.write("\n<!--Add cross=model links -->\n")

        # Add cross-model links  definitions
        k = 1

        while k <= Max_Step_1:
            body = "<rdf:Description rdf:about='" + IRI_prefix + str(base_obj.links_req[i].src_name) + "/'>\n<test_ont:linked_to><rdf:Description rdf:about='" + IRI_prefix + str(base_obj.links_req[i].dist_name) + "/' /></test_ont:linked_to>\n</rdf:Description>\n\n"
            f.write(body)
            i = i + 1
            k = k + 1
            if i >= len(base_obj.links_req): break
        k = 1
        f.write("\n</rdf:RDF>\n")
        f.close()
        spql.write("\nLOAD <file:///" + str(SPARQL_path) + "/" + filename + "_links_" + str(FileNum) + "_.rdf>;\n")
        FileNum = FileNum + 1
    return 1

def inductive_synthesis(src_model_path,link_rules_path, req_model_path, rdf_xml_path, SPARQL_path, IRI_prefix):
    t0 = int(time.time() * 1000)
    tn = t0
    print("Started")
    # Import src model
    src_obj = src_model()
    src_obj.start(src_model_path, model1=[])
    t1 = int(time.time() * 1000)
    print("SRC model imported. Time: " + str(t1 - t0) + " ms.")
    # Create base model
    base_obj = base_model()
    base_obj.start()
    t0 = t1
    t1 = int(time.time() * 1000)
    print("Base model created. Time: " + str(t1 - t0) + " ms.")
    # Add src model
    base_obj.add_model(src_obj)
    t0 = t1
    t1 = int(time.time() * 1000)
    print("SRC model added. Time: " + str(t1 - t0) + " ms.")
    # ID normalisation
    base_obj.id_normalisation()
    t0 = t1
    t1 = int(time.time() * 1000)
    print("Indexes normalized. Time: " + str(t1 - t0) + " ms.")
    # Base links creation
    base_obj.create_base_links(link_rules_path)
    t0 = t1
    t1 = int(time.time() * 1000)
    print("Base links created. Time: " + str(t1 - t0) + " ms.")
    # Create requirements object
    req_obj = req_model()
    req_obj.start(req_model_path, model1=[], base_obj=base_obj)
    t0 = t1
    t1 = int(time.time() * 1000)
    print("Req object created. Time: " + str(t1 - t0) + " ms.")
    # Using requirements
    base_obj.use_requirements()
    t0 = t1
    t1 = int(time.time() * 1000)
    print("Reqs applyed. Time: " + str(t1 - t0) + " ms.")
    # Create links for model_req
    base_obj.create_req_base_links(link_rules_path)
    t0 = t1
    t1 = int(time.time() * 1000)
    print("Req model links created. Time: " + str(t1 - t0) + " ms.")
    t0 = t1
    t1 = int(time.time() * 1000)
    base_np_obj = np.array(base_obj)
    np.save('base_np_obj.npy', base_np_obj)
    rdf_xml_creation(base_obj, rdf_xml_path, SPARQL_path, IRI_prefix)
    print("Models saved. Time: " + str(t1 - t0) + " ms.")
    print("Total time spent: " + str(t1 - tn) + " ms.")
    return 1

if __name__ == "__main__":
    #Example: Inductive synthesis of multilevel model
    #inductive_synthesis("TMP/Test_model.csv", "TMP/Links_rules.csv", "TMP/Test_model.csv", "Hierarchy_model/", "C:/Blazegraph/Load", "http://127.0.0.1/")

    #Example: Inductive synthesis of one-level model
    #inductive_synthesis("TMP/Test_model.csv", "TMP/Links_rules-one-level-TEST.csv", "TMP/Test_model.csv", "Hierarchy_model/", "C:/Blazegraph/Load", "http://127.0.0.1/")

