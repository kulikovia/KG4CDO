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

## Framework files

1. DB_create_script.sql - SQL script for initial DB creation 
2. Deductive_synthesis_(SQL).py - Deductive synthesis program of multilevel KG for the base algorithm
3. Deductive_synthesis_modified(SQL).py - Deductive synthesis program of multilevel KG for the modified algorithm
4. Ind_synthesis_4_(SQL).py - Inductive synthesis program of multilevel KG 
5. Links_rules-one-level-TEST.csv - Ruls for linking private models elements for one-level model
6. Links_rules.csv - Ruls for linking private models elements for hierarchical model
7. Load_comp_KG(hierarhy_3_2-2)_generate_script.py - Script that generates a three-level knowledge graph consisting of two private graph models linked at the second level
8. Load_comp_KG(hierarhy_3_3-3)_generate_script.py - Script that generates a three-level knowledge graph consisting of two private graph models linked at the third level
9. Load_comp_KG(hierarhy_4_2-2)_generate_script.py - Script that generates a four-level knowledge graph consisting of two private graph models linked at the second level
10. Load_comp_KG(hierarhy_5_2-2)_generate_script.py - Script that generates a five-level knowledge graph consisting of two private graph models linked at the second level
11. Load_comp_KG(linear)_generate_script.py - Script that generates model in the format of one-level knowledge graph
12. Model_creation_hierarchy.py - Script that generates hierarchy private graph models
13. Model_creation_one-level.py - Script that generates one-level private graph models
14. Test_template_1-one-level.csv - Template for the Model_creation_one-level.py script
15. Test_template_1.csv - Template for the Model_creation_hierarchy.py script


## Framework structure
The component diagram of the developed framework is shown beow:
![](/images/2.png)

The framework consists of the following components:
1. A package of multilevel knowledge graph synthesis programs, which includes: 

1.1. Inductive synthesis program of multilevel KG}} – Ind_synthesis.py.

**Input data:** Private graph models of SCDO provided by information systems in CSV format (Test_model.csv, columns: MODEL_TYPE (type of private graph model, e.g. access rights system model, network topology model, billing model, etc.), NODE\_TYPE (element type of the private graph model, e.g. network devices and links for the network topology model or user accounts and tariffs for the billing model, etc.), ID (identifier of the element within the private graph model), NAME (name of the element of the private graph model), PARENT_ID (identifier of the parent element of the private graph model), LEVEL_NUM (level number within the private graph model)); rules for linking private graph models in CSV format (Links_rules.csv, columns: SRC_MODEL (name of the type of the first linked model), SRC_ID (element identifier of the first linked model), SRC_NAME (element name of the first linked model), DIST_MODEL (name of the type of the second linked model), DIST_ID (element identifier of the second linked model), DIST_NAME (element name of the second linked model), RULE (name of the linking rule)).

**Output:** The model of the CSDO in the form of a knowledge graph in RDF/XML format and files Model_base.npz, Model_base_links.npz containing the inductive model and Model_base_req.npz, Model_base_links_req.npz containing the inductive model, that takes into account the requirements of users in the format of Numpy data arrays, the runtime of inductive synthesis.

1.2. Deductive synthesis program of multilevel KG for the base algorithm}} – Deductive_synthesis_(SQL).py.

**Input data:** Telecommunication network model in the form of knowledge graph in RDF/XML format and Numpy array; set of facts to be processed in CSV format (Facts.csv, columns: MODEL_TYPE (private graph model type), NODE_TYPE (private graph model element type), FACT_ID (identifier of the fact within the private graph model), NAME (fact name), PARENT_ID (identifier of the parent element of the private graph model), LEVEL_NUM (level number within the private graph model)).

**Output:** Level number at which the model is proved, -1 if the model cannot be proved, deductive synthesis runtime.

1.3. Deductive synthesis program of multilevel KG for the modified algorithm}} – Deductive_synthesis_modified(SQL).py.

**Input data:** Telecommunication network model in the form of knowledge graph in RDF/XML format and Numpy array; single fact to be processed in CSV format (Facts.csv, columns: MODEL_TYPE (private graph model type), NODE_TYPE (private graph model element type), FACT_ID (identifier of the fact within the private graph model), NAME (fact name), PARENT_ID (identifier of the parent element of the private graph model), LEVEL_NUM (level number within the private graph model)); number of the level at which the synthesis time needs to be evaluated.

**Output:** Time to process a single fact, time to perform deductive synthesis at a given level.

1.4. A model data generator that contains the following procedures:

1.4.1. Private model generator of SCDS component models for building a multilevel model – Model_creation_hierarchy.py. 

**Input data:** Private models template in CSV format - Test_template_1.csv. Number of lower level elements of linked models: num_items_1 and num_items_2.

**Output:** Private graph models in CSV format (Test_model.csv, columns: MODEL_TYPE (private graph model type), NODE_TYPE (private graph model element type), ID (element identifier within the private graph model), NAME (private graph model element name), PARENT_ID (parent element identifier of the private graph model), LEVEL_NUM (level number within the private graph model)); set of facts for processing in CSV format (Facts.csv, columns: MODEL_TYPE (private graph model type), NODE_TYPE (private graph model element type), FACT_ID (identifier of the fact within the private graph model), NAME (fact name), PARENT_ID (identifier of the parent element of the private graph model), LEVEL_NUM (level number within the private graph model)).

1.4.2. Private model generator of SSDS component for building a one-level model}} – Model_creation_one-level.py.

**Input data:** Number of elements of model #1 to be linked, number of elements of model #2 to be linked.

**Output:** Private graph models in CSV format (Test_model.csv, columns: \newline MODEL_TYPE (private graph model type), NODE_TYPE (private graph model element type), ID (element identifier within the private graph model), NAME (private graph model element name), PARENT_ID=None and LEVEL_NUM=0 for all the elements of one-level model); set of facts for processing in CSV format (Facts.csv, columns: MODEL_TYPE (private graph model type), NODE_TYPE (private graph model element type), FACT_ID (identifier of the fact within the private graph model), NAME (fact name), PARENT_ID $=$ None and LEVEL_NUM=0 for all the elements of one-level model).

1.4.3. A set of CSDO test model generators in the format of multilevel knowledge graphs for analyzing SPARQL query execution time:

- Load_comp_KG(hierarhy_3_2-2)_generate_script.py is a script that generates a three-level knowledge graph consisting of two private graph models linked at the second level.

- Load_comp_KG(hierarhy_3_3-3)_generate_script.py is a script that generates a three-level knowledge graph consisting of two private graph models linked at the third level.

- Load_comp_KG(hierarhy_4_2-2)_generate_script.py is a script that generates a four-level knowledge graph consisting of two private graph models linked at the second level.

- Load_comp_KG(hierarhy_5_2-2)_generate_script.py is a script that generates a five-level knowledge graph consisting of two private graph models linked at the second level. 

The generator has the following restrictions: the number of linked models is 2, the number of levels of linked models is 3, 4, 5. The structure of generated models is presented in Table below:

| Model #1          |          | Model #2          |          |
|-------------------|----------|-------------------|----------|
| Level 1           | 1        | Level 1           | 1        |
| Level 2           | L2       | Level 2           | L2       |
| Level 3           | L3       | Level 3           | L3       |
| Level 4           | L4       | Level 4           | L4       |
| Level 5           | L5       | Level 5           | L5       |
| Level 6: objects  | M1       | Level 6: objects  | M2       |

**Input data:** The number of elements of the linked private models at each level.

**Output:** The CSDO model in the form of a knowledge graph in RDF/XML format.

1.4.4. Generators of the test CSDO model in the format of one-level knowledge graph for analyzing the speed of SPARQL queries execution – Load_comp_KG(linear)_generate_script.py.

**Input data:** The number of elements of the private models to be linked.

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

5. A Python package for evaluating and comparing knowledge graphs wich also contains a set of SPARQL request is built based on model structure and is aimed to test different request types. A typical set of requests is provided:

5.1. Select an element of the CSDO model by its identifier.

5.2. Select a list of logically related elements of the CSDO model (taking into account hierarchical and single-level connections).

5.3. Select a list of logically related elements of the CSDO model using additional filtering.

5.4. Select a list of logically related elements of the CSDO model using additional filtering and grouping.

5.5. Search for a list of elements by a substring.

## How to use

Below the main steps that should be executed to evaluate the performance of inductive and deductive synthesis algorithms on the example of building five-levels knowledge graph are enumerated: 
1. Generate private graph models. 
To obtain a multilevel knowledge graph, the script **Model_creation_hierarchy.py** should be used. Input parameters are set as script variables: num_objects1, num_objects2 – numbers of elements of linked models at level 6, max_level2 – number of elements of linked models at level 2, max_level3 – number of elements of linked models at level 3, max_level4 – number of elements of linked models at level 4, max_level5 – number of elements of linked models at level 5. It should be noted that for the purposes of forming a symmetric structure of the KG at the upper levels, the data generator provides an equal number of elements at levels 2–5 for linked private graph models. To obtain a one-level knowledge graph it is necessary to use the script **Model_creation_one-level.py**. Input parameters are set as script variables: num_objects1, num_objects2 – number of elements of the linked models.
2. Perform inductive synthesis and estimate its execution time. 
To perform inductive synthesis it is required to use the script  **Ind_synthesis_4_(SQL).py**, Python interpreter version 3 or higher, PostgreSQL version 13 or higher. It is necessary to create a database and to run the SQL script **DB_create_script.sql** in the PostgreSQL console. Input data in the format of CSV files should be located in the same folder with the Python script. Output data is placed in the same folder where the Python script is located; the execution time of synthesis steps is displayed in the console of the Python interpreter.
3. Perform deductive synthesis and estimate its execution time (for basic and modified algorithms). To perform deductive synthesis, it is nesseccary to use the scripts **Deductive_synthesis_(SQL).py** and **Deductive_synthesis_modified(SQL).py**, which require Python interpreter version 3 or higher to run. Input data in CSV file format and arrays in the format provided by the Python module NP, used for working with arrays, must be located in the same folder with the Python script; the number of the level at which the proof occurs is specified via the Python variable of the script max_level. The synthesis time is displayed in the console of the Python interpreter.
4. Analyze the execution time of SPARQL queries to CSDO models.
In order to analyze the execution time of SPARQL queries to the CSDO models in the form of a knowledge graph with different parameters, it is necessary to generate such models using a set of generators: 

4.1. **Load_comp_KG(hierarhy_3_2-2)_generate_script.py**, 

4.2. **Load_comp_KG(hierarhy_3_3-3)_generate_script.py**, 

4.3. **Load_comp_KG(hierarhy_4\_2-2)_generate_script.py**, 

4.4. **Load_comp_KG(hierarhy_5_2-2)_generate_script.py**,

4.5. **Load_comp_KG(linear)_generate_script.py**. 

The Python interpreter version 3 or higher is required to run the scripts. Model parameters are set via the following script variables: max_level_2, max_level_3, max_level_4, max_level_5, max_objects1 and max_objects2. The resulting models in RDF/XML format are loaded into the RDF data repository using standard data storage methods. We used Blazegraph. Queries were executed from the standard Web application Blazegraph which provides a screen display of the execution time of each SPARQL query.

## Experiments

### Synthesis of Multilevel knowledge graphs: Methods and technologies for dynamic networks

In this [article](https://www.sciencedirect.com/science/article/pii/S0952197623004281) we present a real two [realistic datasets](https://zenodo.org/records/7605504) (namely, for SPARQL querying performance analysis, and for our case study on dynamic network monitoring). Our experiments show that the developed models of multilevel synthesis reduce the time complexity up to 73% on practice compared to the baselines, and are lossless and able to beat their competitors based on parallel knowledge graph processing from 4% to 91% in terms of computational time (depending on the query type). Further parallelisation of our multilevel models is even more efficient (the reduction of query processing time is about 40%–45%) and opens promising prospects for the creation and exploitation of dynamic Knowledge Graphs in practice.

## References

## Patch Note / Major Updates

