# KG4CDO: A Knowledge Based Framework for Objects Models Synthesis

[KG4CDO website](https://github.com/kulikovia/KG4CDO)

## Contributors

Correspondence to: 
  - [Igor Kulikov](http://) (i.a.kulikov@gmail.com)
  - [Nataly Zhukova](https://) (nazhukova@mail.ru)
  - [Man Tianxing](https://) (mantx@jlu.edu.cn)
  
## Paper

[**Synthesis of multilevel knowledge graphs: Methods and technologies for dynamic networks**](https://www.sciencedirect.com/science/article/pii/S0952197623004281)<br>
Tianxing Man, Alexander Vodyaho, Dmitry I. Ignatov, Igor Kulikov, Nataly Zhukova<br>
Engineering Applications of Artificial Intelligence, 2023. Connected research.

If you find this repository useful, please cite our paper and corresponding framework:
```
@misc{Man_Vodyaho_Ignatov_Kulikov_Zhukova_2023, 
	title={Synthesis of multilevel knowledge graphs: Methods and technologies for dynamic networks}, 
	volume={123}, 
	url={http://dx.doi.org/10.1016/j.engappai.2023.106244}, 
	DOI={10.1016/j.engappai.2023.106244}, 
	journal={Engineering Applications of Artificial Intelligence}, 
	publisher={Elsevier BV}, 
	author={Man, Tianxing and Vodyaho, Alexander and Ignatov, Dmitry I. and Kulikov, Igor and Zhukova, Nataly}, 
	year={2023}, 
	month=aug, 
	language={en} }
```


## Framework structure
The component diagram of the developed framework is shown beow:
![](/images/2.png)

The framework consists of the following methods and functions:
1. A package of multilevel knowledge graph synthesis programs, which includes: 

1.1. Inductive synthesis method of multilevel KG

    inductive_synthesis(src_model_path,link_rules_path, req_model_path, rdf_xml_path, SPARQL_path, IRI_prefix)


**Input data:** _src_model_path_ - the path to the private graph models of SCDO provided by information systems in CSV format, columns: MODEL_TYPE (type of private graph model, e.g. access rights system model, network topology model, billing model, etc.), NODE\_TYPE (element type of the private graph model, e.g. network devices and links for the network topology model or user accounts and tariffs for the billing model, etc.), ID (identifier of the element within the private graph model), NAME (name of the element of the private graph model), PARENT_ID (identifier of the parent element of the private graph model), LEVEL_NUM (level number within the private graph model)); _link_rules_path_ - the path to the file with rules for linking private graph models in CSV format, columns: SRC_MODEL (name of the type of the first linked model), SRC_ID (element identifier of the first linked model), SRC_NAME (element name of the first linked model), DIST_MODEL (name of the type of the second linked model), DIST_ID (element identifier of the second linked model), DIST_NAME (element name of the second linked model), RULE (name of the linking rule)); _req_model_path_ - the path to the user requirements in CSV format, columns: MODEL_TYPE (type of private graph model, e.g. access rights system model, network topology model, billing model, etc.), NODE\_TYPE (element type of the private graph model, e.g. network devices and links for the network topology model or user accounts and tariffs for the billing model, etc.), ID (identifier of the element within the private graph model), NAME (name of the element of the private graph model), PARENT_ID (identifier of the parent element of the private graph model), LEVEL_NUM (level number within the private graph model)); _rdf_xml_path_ - the path to the RDF/XML folder where KG files are collected; SPARQL_path - the path from wich RDF/XML data is loaded to RDF storage; IRI_prefix - prefix for using ontology (i.e. "http://www.w3.org/2001/vcard-rdf/3.0#").

**Output:** The model of the CSDO in the form of a knowledge graph in the following formats: Base.csv - nodes of inductive model, Req.csv - nodes of user model, files in RDF/XML format are collected in the _rdf_xml_path_ and file base_np_obj.npy containing the inductive model, that takes into account the requirements of users in the format of Numpy data arrays.

1.2. Deductive synthesis program of multilevel KG for the base algorithm

	deductive_synthesis(model_req_path, facts_path, max_level)

**Input data:** _model_req_path_ - the path to the user model in CSV format (i.e. Req.csv - nodes of user model); _facts_path_ - the path to the set of facts to be processed in CSV format (Facts.csv, columns: MODEL_TYPE (private graph model type), NODE_TYPE (private graph model element type), FACT_ID (identifier of the fact within the private graph model), NAME (fact name), PARENT_ID (identifier of the parent element of the private graph model), LEVEL_NUM (level number within the private graph model)); _max_level_ - number of levels in the user model.

**Output:** Level number at which the model is proved, -1 if the model cannot be proved, deductive synthesis runtime.



1.3. Deductive synthesis program of multilevel KG for the modified algorithm

	deductive_synthesis_modified(model_req_path, singl_fact_path)

**Input data:** _model_req_path_ - the path to the user model in CSV format (i.e. Req.csv - nodes of user model); _singl_fact_path_ - the path to the single fact to be processed in CSV format (Facts.csv, columns: MODEL_TYPE (private graph model type), NODE_TYPE (private graph model element type), FACT_ID (identifier of the fact within the private graph model), NAME (fact name), PARENT_ID (identifier of the parent element of the private graph model), LEVEL_NUM (level number within the private graph model)).

**Output:** Time to process a single fact, time to perform deductive synthesis at a given level.

1.4. A model data generator that contains the following procedures:

1.4.1. Private universal model generators of SCDS component models for building a multilevel model. Universal model contains not customised automatically generated models and elements names.

The multi-level knowledge graph structure  is shown beow:
![](/images/4.png)

	Function for the full model generation.

	create_uni_model(levels_number, elements_number, distribution_type, partial_models_number, linking_level, linking_rules)

**Input data:** levels_number - number of partial models levels; elements_number - each partial model elements number; distribution_type - the one of distribution type for elements thruth levels ("uniform", "linear", "quadratic", "exponential"); partial_models_number - number of partial models; linking_level - on which level the partial models is linked; linking_rules - string with linking rules separated with ';' e.g. "1-2;2-3" (partial model 1 is linked to partial model 2 and partial model 2 is linked to partial model 3).

**Output:** Private graph models in CSV format (Test_model.csv, columns: MODEL_TYPE (private graph model type), NODE_TYPE (private graph model element type), ID (element identifier within the private graph model), NAME (private g, "quadratic", "exponential"); raph model element name), PARENT_ID (parent element identifier of the private graph model), LEVEL_NUM (level number within the private graph model)); set of facts for processing in CSV format (Facts.csv, columns: MODEL_TYPE (private graph model type), NODE_TYPE (private graph model element type), FACT_ID (identifier of the fact within the private graph model), NAME (fact name), PARENT_ID (identifier of the parent element of the private graph model), LEVEL_NUM (level number within the private graph model)).


	Function for the model generation for the selected level.
	
	create_uni_model_for_One_level(levels_number, elements_number, distribution_type, partial_models_number, linking_level, linking_rules, selected_level)

**Input data:** levels_number - number of partial models levels; elements_number - each partial model elements number; distribution_type - the one of distribution type for elements thruth levels ("uniform", "linear", "quadratic", "exponential"); partial_models_number - number of partial models; linking_level - on which level the partial models is linked; linking_rules - string with linking rules separated with ';' e.g. "1-2;2-3" (partial model 1 is linked to partial model 2 and partial model 2 is linked to partial model 3); selected_level - the number of selected level.

**Output:** Private graph models in CSV format (Test_model.csv, columns: MODEL_TYPE (private graph model type), NODE_TYPE (private graph model element type), ID (element identifier within the private graph model), NAME (private g, "quadratic", "exponential"); raph model element name), PARENT_ID (parent element identifier of the private graph model), LEVEL_NUM (level number within the private graph model)); set of facts for processing in CSV format (Facts.csv, columns: MODEL_TYPE (private graph model type), NODE_TYPE (private graph model element type), FACT_ID (identifier of the fact within the private graph model), NAME (fact name), PARENT_ID (identifier of the parent element of the private graph model), LEVEL_NUM (level number within the private graph model)).


	Function for the model generation for a list of selected levels.

	create_uni_model_for_List_levels(levels_number, elements_number, distribution_type, partial_models_number, linking_level, linking_rules, levels_list)

**Input data:** levels_number - number of partial models levels; elements_number - each partial model elements number; distribution_type - the one of distribution type for elements thruth levels ("uniform", "linear", "quadratic", "exponential"); partial_models_number - number of partial models; linking_level - on which level the partial models is linked; linking_rules - string with linking rules separated with ';' e.g. "1-2;2-3" (partial model 1 is linked to partial model 2 and partial model 2 is linked to partial model 3); levels_list - the list of the selected levels (i.e. "1;2;3").

**Output:** Private graph models in CSV format (Test_model.csv, columns: MODEL_TYPE (private graph model type), NODE_TYPE (private graph model element type), ID (element identifier within the private graph model), NAME (private g, "quadratic", "exponential"); raph model element name), PARENT_ID (parent element identifier of the private graph model), LEVEL_NUM (level number within the private graph model)); set of facts for processing in CSV format (Facts.csv, columns: MODEL_TYPE (private graph model type), NODE_TYPE (private graph model element type), FACT_ID (identifier of the fact within the private graph model), NAME (fact name), PARENT_ID (identifier of the parent element of the private graph model), LEVEL_NUM (level number within the private graph model)).


1.4.2. Private cusmom model generators of SCDS component models for building a multilevel model. Custom model contains generated models and elements names defined by user.

	Function for the full model generation.

	create_cust_model(levels, elements_number, distribution_type, models, linking_level, linking_rules)

**Input data:** levels - 2-dimension array with levels names for every private model; elements_number - each partial model elements number; distribution_type - the one of distribution type for elements thruth levels ("uniform", "linear", "quadratic", "exponential"); models - array with models names; linking_level - on which level the partial models is linked; linking_rules - string with linking rules separated with ';' e.g. "1-2;2-3" (partial model 1 is linked to partial model 2 and partial model 2 is linked to partial model 3).

	Useful examples:
	models = ['Access_Network_Subsystem', 'Core_Network_Subsystem']

	levels = [['Geographic_region', 'Geo_sub-region_Level_1', 'Accessed_Device_Layer_1_Unit_(connection_layer)', 'Accessed_Device_Layer_2_Unit', 'Accessed_Device'],
          ['Domain', 'Sub-Domain_Level_1_Unit', 'Sub-Domain_Level_2_Unit', 'Sub-Domain_Level_4_Unit_(connection_layer)', 'Sub-Domain_Level_5_Unit', 'Core_Device']]
    

**Output:** Private graph models in CSV format (Test_model.csv, columns: MODEL_TYPE (private graph model type), NODE_TYPE (private graph model element type), ID (element identifier within the private graph model), NAME (private g, "quadratic", "exponential"); raph model element name), PARENT_ID (parent element identifier of the private graph model), LEVEL_NUM (level number within the private graph model)); set of facts for processing in CSV format (Facts.csv, columns: MODEL_TYPE (private graph model type), NODE_TYPE (private graph model element type), FACT_ID (identifier of the fact within the private graph model), NAME (fact name), PARENT_ID (identifier of the parent element of the private graph model), LEVEL_NUM (level number within the private graph model)).


	Function for the model generation for the selected level.
	
	create_cust_model_for_One_level(levels, elements_number, distribution_type, models, linking_level, linking_rules, selected_level)

**Input data:** levels - 2-dimension array with levels names for every private model; elements_number - each partial model elements number; distribution_type - the one of distribution type for elements thruth levels ("uniform", "linear", "quadratic", "exponential"); models - array with models names; linking_level - on which level the partial models is linked; linking_rules - string with linking rules separated with ';' e.g. "1-2;2-3" (partial model 1 is linked to partial model 2 and partial model 2 is linked to partial model 3); selected_level - the number of selected level.

**Output:** Private graph models in CSV format (Test_model.csv, columns: MODEL_TYPE (private graph model type), NODE_TYPE (private graph model element type), ID (element identifier within the private graph model), NAME (private g, "quadratic", "exponential"); raph model element name), PARENT_ID (parent element identifier of the private graph model), LEVEL_NUM (level number within the private graph model)); set of facts for processing in CSV format (Facts.csv, columns: MODEL_TYPE (private graph model type), NODE_TYPE (private graph model element type), FACT_ID (identifier of the fact within the private graph model), NAME (fact name), PARENT_ID (identifier of the parent element of the private graph model), LEVEL_NUM (level number within the private graph model)).


	Function for the model generation for a list of selected levels.

	create_cust_model_for_List_levels(Levels, elements_number, distribution_type, Models, linking_level, linking_rules, levels_list)

**Input data:** levels - 2-dimension array with levels names for every private model; elements_number - each partial model elements number; distribution_type - the one of distribution type for elements thruth levels ("uniform", "linear", "quadratic", "exponential"); models - array with models names; linking_level - on which level the partial models is linked; linking_rules - string with linking rules separated with ';' e.g. "1-2;2-3" (partial model 1 is linked to partial model 2 and partial model 2 is linked to partial model 3); levels_list - the list of the selected levels (i.e. "1;2;3").

**Output:** Private graph models in CSV format (Test_model.csv, columns: MODEL_TYPE (private graph model type), NODE_TYPE (private graph model element type), ID (element identifier within the private graph model), NAME (private g, "quadratic", "exponential"); raph model element name), PARENT_ID (parent element identifier of the private graph model), LEVEL_NUM (level number within the private graph model)); set of facts for processing in CSV format (Facts.csv, columns: MODEL_TYPE (private graph model type), NODE_TYPE (private graph model element type), FACT_ID (identifier of the fact within the private graph model), NAME (fact name), PARENT_ID (identifier of the parent element of the private graph model), LEVEL_NUM (level number within the private graph model)).


1.4.3. Private universal model generator of SSDS component for building a one-level model. Universal model contains not customised automatically generated models and elements names.

	create_One_level_model(partial_models_number, elements_number)

**Input data:** elements_number - each partial model elements number; distribution_type - the one of distribution type for elements thruth levels ("uniform", "linear", "quadratic", "exponential"); partial_models_number - number of partial models.

**Output:** Private graph models in CSV format (Test_model.csv, columns: \newline MODEL_TYPE (private graph model type), NODE_TYPE (private graph model element type), ID (element identifier within the private graph model), NAME (private graph model element name), PARENT_ID=None and LEVEL_NUM=0 for all the elements of one-level model); set of facts for processing in CSV format (Facts.csv, columns: MODEL_TYPE (private graph model type), NODE_TYPE (private graph model element type), FACT_ID (identifier of the fact within the private graph model), NAME (fact name), PARENT_ID $=$ None and LEVEL_NUM=0 for all the elements of one-level model).

1.4.4. The CSDO test model generators in the format of multilevel knowledge graphs for analyzing SPARQL query execution time.

	Function that generates universal model as multi-level knowledge graph. Universal model contains not customised automatically generated models and elements names.
	
	createRDF_universal(filename, levels_number, elements_number, distribution_type, partial_models_number, linking_level, linking_rules, SPARQL_path, Model_path, IRI_prefix, isDynamic=False, start_date=None, end_date=None, dynamic_levels_elements_number=None, value_min=0, value_max=100)
	
**Input data:** filename - model file name; levels_number - number of partial models levels; elements_number - each partial model elements number; distribution_type - the one of distribution type for elements thruth levels ("uniform", "linear", "quadratic", "exponential"); partial_models_number - number of partial models; linking_level - on which level the partial models is linked; linking_rules - string with linking rules separated with ';' e.g. "1-2;2-3" (partial model 1 is linked to partial model 2 and partial model 2 is linked to partial model 3); SPARQL_path - the path from wich RDF/XML data is loaded to RDF storage; IRI_prefix - prefix for using ontology (i.e. "http://www.w3.org/2001/vcard-rdf/3.0#"), Model_path - the path to the directory for collecting RDF/XML files; isDynamic - is dynamic data has to be added (True/False, defaulf: isDynamic=False); start_date - start date of dynamic data period e.g. "2025-01-01", default: start_date=None; end_date - end date of dynamic data period e.g. "2025-01-02", default: end_date=None; dynamic_levels_elements_number - string with dynamic data distribution rules separated with ';' e.g. "1-100;2-300" (100 dynamic events on the level 1 and 300 dynamic events on the level 2) default: dynamic_levels_elements_number=None; value_min - minimum value of the dynamic parameter, default: value_min=0; value_max - maximum value of the dynamic parameter, default: value_max=100.

**Output:** The CSDO model in the form of a knowledge graph in RDF/XML format.

	Function that generates custom model as multi-level knowledge graph. Custom model contains models and elements names defined by user.
	
	createRDF_domain(filename, levels, elements_number, distribution_type, models, linking_level, linking_rules, SPARQL_path, Model_path, IRI_prefix, isDynamic=False, start_date=None, end_date=None, dynamic_levels_elements_number=None, value_min=0, value_max=100)
	

**Input data:** filename - model file name; levels - 2-dimension array with levels names for every private model; elements_number - each partial model elements number; distribution_type - the one of distribution type for elements thruth levels ("uniform", "linear", "quadratic", "exponential"); models - array with models names; linking_level - on which level the partial models is linked; linking_rules - string with linking rules separated with ';' e.g. "1-2;2-3" (partial model 1 is linked to partial model 2 and partial model 2 is linked to partial model 3); SPARQL_path - the path from wich RDF/XML data is loaded to RDF storage; IRI_prefix - prefix for using ontology (i.e. "http://www.w3.org/2001/vcard-rdf/3.0#"), Model_path - the path to the directory for collecting RDF/XML files; isDynamic - is dynamic data has to be added (True/False, defaulf: isDynamic=False); start_date - start date of dynamic data period e.g. "2025-01-01", default: start_date=None; end_date - end date of dynamic data period e.g. "2025-01-02", default: end_date=None; dynamic_levels_elements_number - string with dynamic data distribution rules separated with ';' e.g. "1-100;2-300" (100 dynamic events on the level 1 and 300 dynamic events on the level 2) default: dynamic_levels_elements_number=None; value_min - minimum value of the dynamic parameter, default: value_min=0; value_max - maximum value of the dynamic parameter, default: value_max=100.

	Useful examples:
	models = ['Access_Network_Subsystem', 'Core_Network_Subsystem']

	levels = [['Geographic_region', 'Geo_sub-region_Level_1', 'Accessed_Device_Layer_1_Unit_(connection_layer)', 'Accessed_Device_Layer_2_Unit', 'Accessed_Device'],
          ['Domain', 'Sub-Domain_Level_1_Unit', 'Sub-Domain_Level_2_Unit', 'Sub-Domain_Level_4_Unit_(connection_layer)', 'Sub-Domain_Level_5_Unit', 'Core_Device']]


**Output:** The CSDO model in the form of a knowledge graph in RDF/XML format.


1.4.5. Generator of the universal test CSDO model in the format of one-level knowledge graph for analyzing the speed of SPARQL queries execution

	createRDF_universal_One_level(filename, partial_models_number, elements_number, linking_rules, SPARQL_path, Model_path, IRI_prefix, isDynamic=False, start_date=None, end_date=None, value_min=0, value_max=100, elements_number_dynamic=100)


**Input data:** filename - model file name; elements_number - each partial model elements number; partial_models_number - number of partial models; linking_rules - string with linking rules separated with ';' e.g. "1-2;2-3" (partial model 1 is linked to partial model 2 and partial model 2 is linked to partial model 3); SPARQL_path - the path from wich RDF/XML data is loaded to RDF storage; IRI_prefix - prefix for using ontology (i.e. "http://www.w3.org/2001/vcard-rdf/3.0#"), Model_path - the path to the directory for collecting RDF/XML files; isDynamic - is dynamic data has to be added (True/False, defaulf: isDynamic=False); start_date - start date of dynamic data period e.g. "2025-01-01", default: start_date=None; end_date - end date of dynamic data period e.g. "2025-01-02", default: end_date=None; elements_number_dynamic - number of dynamic elements, default: elements_number_dynamic=100; value_min - minimum value of the dynamic parameter, default: value_min=0; value_max - maximum value of the dynamic parameter, default: value_max=100.

**Output:** The CSDO model in the form of a knowledge graph in RDF/XML format. 

2. Knowledge graph component including:

2.1. A graph DBMS with SPARQL 1.1 support;

2.2. Ontology repository;

2.3. Dynamic REST service for organizing interaction with external systems.

3. Relational DBMS PostgreSQL.

4. File system for storing input and output data in file formats. The file system is used in the following cases:

4.1. Inductive and Deductive Synthesis programs perform reading of private graph models and operational data about TNs from files placed in the File System;

4.2. Inductive synthesis program generates TN models in RDF/XML format and places them as files in the File System;

4.3. Inductive and Deductive Synthesis programs save their logs in the File System;

4.4. Inductive and Deductive Synthesis programs use PostgreSQL relational DBMS to implement operations on data tables and store intermediate results;

4.5. Loading models and operational data into the graph data store is performed from RDF/XML files hosted in the File System. 

5. A Python package for evaluating and comparing knowledge graphs wich also contains a set of SPARQL request is built based on model structure and is aimed to test different request types. 


## How to use

Below the main steps that should be executed to evaluate the performance of inductive and deductive synthesis algorithms on the example of building five-levels knowledge graph are enumerated: 
1. Install the Python library kg4cdo:

	**pip install kg4cdo**

2. Generate private graph models. 

To obtain a multilevel knowledge graph, the one of the functions **create_uni_model** or **create_cust_model** should be used. 

	Examples:
	
	create_uni_model(5,50,"exponential", 2, 3, "1-2")
	
	create_cust_model(Levels,100000,"exponential", Models, 5, "1-2;2-3;3-4;4-5;5-6;6-7;7-8;8-9;9-10")

To obtain a multilevel knowledge graph only for a one selected level, the one of the functions **create_uni_model_for_One_level** or **create_cust_model_for_One_level** should be used.

	Examples:
	
	create_uni_model_for_One_level(10, 100000, "exponential", 5, 5, "1-2;2-3;3-4;4-5", 1)
	
	create_cust_model_for_One_level(Levels, 100000, "exponential", Models, 5, "1-2;2-3;3-4;4-5", 1)

To obtain a multilevel knowledge graph for a list of selected levels, the one of the functions **create_uni_model_for_List_levels** or **create_cust_model_for_List_levels** should be used.

	Examples:
	
	create_uni_model_for_List_levels(5, 50, "exponential", 1, 5, "1-2;2-3;3-4;4-5;5-6;6-7;7-8;8-9;9-10", "9;10")
	
	create_cust_model_for_List_levels(Levels, 100000, "exponential", Models, 5, "1-2;2-3;3-4;4-5;5-6;6-7;7-8;8-9;9-10", "9;10")

3. Perform inductive synthesis and estimate its execution time. 

To perform inductive synthesis it is required to use the function  **inductive_synthesis**

	Example:
	
	inductive_synthesis("TMP/Test_model.csv", "TMP/Links_rules.csv", "TMP/Test_model.csv", "Hierarchy_model/", "C:/Blazegraph/Load", "http://127.0.0.1/")

4. Perform deductive synthesis and estimate its execution time (for basic and modified algorithms). To perform deductive synthesis, it is nesseccary to use the functions **deductive_synthesis** and **deductive_synthesis_modified**.

	Examples:
	
	deductive_synthesis('Req.csv', 'TMP/Test_facts1.csv', 5)
	deductive_synthesis_modified('Req.csv', 'TMP/Test_facts1.csv')

5. Analyze the execution time of SPARQL queries to CSDO models.
In order to analyze the execution time of SPARQL queries to the CSDO models in the form of a knowledge graph with different parameters, it is necessary to generate such models using the generators: 

5.1. **createRDF_universal** or **createRDF_domain**. 

	Examples:
	
	createRDF_universal("KG_data", 6,100,"exponential", 3, 3, "1-2;2-3", "C:/Blazegraph/Load", "Hierarchy_model/", "http://127.0.0.1/ont_test#",False, '2025-08-01', '2025-08-02', '2-10;3-10;4-10')
	
	createRDF_domain("KG_data", Levels, 100000, "exponential", Models, 5, "1-2;2-3;3-4;4-5;5-6;6-7;7-8;8-9;9-10", "C:/Blazegraph/Load", "Hierarchy_model/", "http://127.0.0.1/ont_test#",False, '2025-08-01', '2025-08-02', '2-10;3-10;4-10')

5.2. **createRDF_universal_One_level**.

	Example:
	
	createRDF_universal_One_level("KG_data", 5, 10, "1-2;2-3;3-4;4-5", "C:/Blazegraph/Load", "Linear_model/", "http://127.0.0.1/ont_test#", isDynamic=True, start_date='2025-09-10', end_date='2025-09-18', value_min=0, value_max=100, elements_number_dynamic=100)

## Experiments

### Synthesis of Multilevel knowledge graphs: Methods and technologies for dynamic networks

In this [article](https://www.sciencedirect.com/science/article/pii/S0952197623004281) we present a real two [realistic datasets](https://zenodo.org/records/7605504) (namely, for SPARQL querying performance analysis, and for our case study on dynamic network monitoring). Our experiments show that the developed models of multilevel synthesis reduce the time complexity up to 73% on practice compared to the baselines, and are lossless and able to beat their competitors based on parallel knowledge graph processing from 4% to 91% in terms of computational time (depending on the query type). Further parallelisation of our multilevel models is even more efficient (the reduction of query processing time is about 40%–45%) and opens promising prospects for the creation and exploitation of dynamic Knowledge Graphs in practice.


## References

## Patch Note / Major Updates

