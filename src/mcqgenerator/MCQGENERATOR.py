import os
import json
import pandas as pd
import traceback
import g4f
from g4f.client import Client 
from langchain.prompts import PromptTemplate
from src.mcqgenerator.looger import logging
from src.mcqgenerator.utils import read_file,get_table_data



TEMPLATE="""
You are an expert the medical field.Given the symptoms {symptoms} for each patient, it is your job to \
create a paragraph of {number} 5 for each patient {patient} in which you will mention the disease and the potential treatments or medicines.
Consider that this patient has a{tone} tone to understand medical concepts Make sure to be precise and speak in his {tone}.You have 3 main {tone}: easy, \
intermediate and advanced.Explain the disease in the {tone} given.
"""

TEMPLATE2 = """
You are a highly skilled medical expert. Given the following completion output:
"{diagnosis_output}"
1. Extract the patient names and their diagnosed diseases. List them in this format:
   - Patient - Diagnosed Disease -.
   - Patient - Diagnosed Disease.
   - Patient - Diagnosed Disease .
   [Repeat as needed for additional patients.]

2. Analyze the gravity of each disease. Provide a short note (in 5 sentences) about the severity and chronicity of each disease.

3. Based on the chronicity and severity, conclude which patient needs urgent medical attention. Clearly state which patient requires the most immediate care, along with the reason.

Provide the results in the following format:
- Patient List: 
   - Patient List with diseases
- Disease Severity Notes: 
   - Severity notes for each patient’s disease
- Conclusion: The patient who needs urgent attention is given as an output with the reason and explanation.

"""

diagnosis_generation_prompt=PromptTemplate(
    input_variables=["number","symptoms","patient","tone"],
    template=TEMPLATE
    )
Evaluation_generation_prompt=PromptTemplate(
    input_variables=["diagnosis_output"],
    template=TEMPLATE2
    )

client=Client()
def completions(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}]
    )
    print(response.choices[0].message.content)

def completion_evaluation(response_message):
    evaluation_message = Evaluation_generation_prompt.format(
        diagnosis_output=response_message
        )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": evaluation_message}]
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content
response_message = diagnosis_generation_prompt.format(
    number=5,
    symptoms=[["Abdominal pain and cramping","Chronic diarrhea","Fatigue"],["Severe headaches","Blurred vision","Nausea and vomiting"],["Chest pain","Shortness of breath","Rapid heart rate"],["Persistent cough","Unexplained weight loss","Night sweats"]],
    patient=["karim","Amina","Yassine","Sara"],
    tone=["advanced","advanced","advanced","advanced"]
)
completions(response_message)
evaluation_message = Evaluation_generation_prompt.format(
    diagnosis_output=response_message
)

completions(evaluation_message)