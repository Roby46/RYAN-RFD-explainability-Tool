# RFD Explainability Insight Navigator (REIN)

The RFD Explainability Insight Navigator (REIN) tool is one of the first AI-based tools that analyzes how RFDs discovered on a dataset evolve as the data changes. REIN is able to combine interactive visual components and emergent Large Language Models (LLMs) to provide explanations for expert and non-expert users about the meaningfulness of discovered RFDs before and after data changes.

## Requirements

In a python environment, install the following libraries:
```bash
  pip install csv
  pip install json
  pip install copy
  pip install numpy
  pip install requests
  pip install flask
  pip install flask_CORS
  pip install Pandas
  pip install gpt4all
```

## Data pre-processing
 
Before the REIN tool can be used to analyse the RFDs, it is necessary to construct the .json files containing all the information from the comparison of the RFDs sets discovered. These files are constructed via the python script 'jsonForChartCreator_v3'.

#### Input of the "jsonForChartCreator_v3.py" script

this script takes as input two separate files:

    1) the file of RFDs discovered at a given instant of time
    2) the file of RFDs discovered at a different instant of time

Both files must be in .csv format and respect the following formatting:

    RHS;attributeA;attributeB;attributeC;.....attributeN
    attributeA;thr;thr;............
    ....
    attributeX;thr;thr;............

EXAMPLE: I have the dependency A,B ---> C with thresholds thr(A) = 2, thr(B) = 4 and thr(C) = 1. In the RFDs file, this RFD will be represented like this

    RHS;A;B;C;D;E;F
    C;2;4;1;?;?;?

With the first column containing the name of the RHS attribute and the remaining columns containing the threshold values of the attributes involved in the dependency. For those that are not involved, enter the '?' in the relevant cell. Example files are provided in the repository.

The execution of this script allows the creation of the .json files required for dependency analysis. Your files will be saved in the paths "./static/json_chart" and "./static/json_percentages".

#### Structure of the dataset file

As for the dataset file, which is required for the explainability of the dependencies, the file type must be a csv, with the first line containing the dataset header and the remaining lines containing all the tuples of the dataset on which the RFD discovery algorithms have been applied. In addition, tuples that result in deletions must be duplicated at the end of the dataset.

As regards the content of the file, it is important to note that, in addition to the columns relating to the attributes of the dataset, two other columns must be present: 'operation' and 'index'.

The 'operation' column can take on three distinct values: 0, 1 and -1. The value 0 is assigned to all the tuples in the dataset; the value 1, on the other hand, is assigned to all the tuples that are insertions with respect to the first considered time instant. The value -1, on the other hand, is to be assigned to all copies of tuples that are considered to be deletions.

As regards the 'index' column, on the other hand, the value of this attribute may be 0 (for all tuples in the dataset) or it may take a value equal to the index of the deleted tuple (this index value is to be set only for duplicates of these tuples). 

EXAMPLE: Assuming we have, at time instant t1, a dataset of 5 tuples, with attributes A, B and C.

    A;B;C
    1;1;1
    2;2;2
    3;3;3
    4;4;4
    5;5;5

Suppose that, at time t2, the tuple (3;3;3) is deleted and a new tuple (6;6;6) is added. The dataset file will look like this:

    A;B;C;operation;index
    1;1;1;0;0
    2;2;2;0;0
    3;3;3;0;0
    4;4;4;0;0
    5;5;5;0;0
    6;6;6;1;0
    3;3;3;-1;2

In the repository, you can find an example file in the Dataset folder.

