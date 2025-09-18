
def create_One_level_model(partial_models_number, elements_number):
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
        body = "Model_" + str(i_model) + ",Model_" + str(i_model) + "_Element_level_0,0," + "Model_" + str(
            i_model) + "_Core_node,,0\n"
        model_csv.write(body)
        facts1_csv.write(body)
        facts2_csv.write(body)
        i = 1
        model_counter = 1
        while model_counter <= elements_number:
            body = "Model_" + str(i_model) + ",Model_" + str(i_model) + "_Element_level_1," + str(i) + ",Model_" + str(i_model) + "_Element_level_1" + "_" + str(i) + ",0\n"
            model_csv.write(body)
            facts1_csv.write(body)
            facts2_csv.write(body)
            i = i + 1
            model_counter = model_counter + 1

    # Close file
    model_csv.close()
    facts1_csv.close()
    facts2_csv.close()

    return 1

if __name__ == "__main__":
    create_One_level_model(10,10)