import requests
import csv
from flask import Flask, redirect, url_for, request, jsonify, render_template
from flask_cors import CORS
from io import BytesIO
import pandas as pd
from StarDust import PatternLoader
import sys
import numpy as np
import copy
import llm_interaction as llm


model = llm.load_model()
print("Large Language Model",model)

context_spec='''In relational databases, a Relaxed Functional Dependency (RFD) is an integrity constraint X -> Y 
   between two sets of attributes X and Y, meaning that if two tuples have similar value on X, then they must have similar values on Y.
   X is named Left Hand Side (LHS), while Y is the Right Hand Side (RHS). Two values of an attribute are similar if their distance is 
   lower than the similarity threshold defined on that attribute. The function to assess similarity is edit distance for strings and difference for numbers.
   
   After the insertion of a new tuple, an existing RFD can be invalidated only if the new tuple has similar values on the LHS with respect other tuples but 
   it has different values on the RHS.  In this case, a specialized RFD with additional attributes on the LHS may be valid on the dataset. 
'''

detail_spec='''
   You will be provided with an RFD that gets invalidated after the insertion of a batch of tuples, and with the tuples that caused the violation and their values. 

   The RFD = {LHS: ["Journal(threshold=1)"], RHS: ["Volume(threshold=5)"].} was invalidated and specialized by the new RFD {LHS:  ["Journal(threshold=1)", Citations(threshold=2)], RHS: ["Volume(threshold=5)"].}
   This happened because:
   - The insertion of Tuple 1 (Journal=Nature, Volume=4) caused a violation considering tuple 3 (Journal=Natures, Volume=16).
   - The insertion of Tuple 2 (Journal=Science, Volume=10) caused a violation considering tuple 4 (Journal=Sciences, Volume=1).

   Basing on this information, provide an extensive explanation of why the RFD was invalidated.
   To do this, analyze the attribute values and consider the similarity thresholds. 
'''

context_gen='''In relational databases, a Relaxed Functional Dependency (RFD) is an integrity constraint X -> Y 
   between two sets of attributes X and Y, meaning that if two tuples have similar value on X, then they must have similar values on Y.
   X is named Left Hand Side (LHS), while Y is the Right Hand Side (RHS). Two values of an attribute are similar if their distance is 
   lower than the similarity threshold defined on that attribute. The function to assess similarity is edit distance for strings and difference for numbers.
   
   After the deletion of a tuple, an existing RFD can be no longer minimal if the deleted tuple had similar values on the LHS with respect other tuples but 
   it had different values on the RHS. In this case, a generalized RFD with a subset of attributes on the LHS may be valid on the dataset. 
'''


detail_gen='''
   You will be provided with an RFD that gets generalized after the deletion of a batch of tuples. 
   You will be provided with the tuples that caused the generalization and their values. 

   Generalized RFD = LHS: ["Journal(threshold=1)", "Author(threshold=3)"], RHS: ["Volume(threshold=2)"]. 

   This happened because:
   - Tuple 1 (Journal=Nature, Author=Cirillo, Volume=4), which caused a violation considering tuple 3 (Journal=Natures, Author=Cirillo, Volume=16), has been removed.
   - Tuple 2 (Journal=Science,  Author=Caruccio, Volume=10), which caused a violation considering tuple 4 (Journal=Sciences, Author=Caruccio, Volume=1) has been removed.

   Basing on this information, provide an extensive explanation of why the RFD was generalized.
   To do this, analyze the attribute values and consider the similarity thresholds. 
'''

prompt= context_spec + detail_spec

output = llm.ask_llm(model, prompt, max_tokens=300, streaming=False)

print(output)
