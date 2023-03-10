import streamlit as st
import boto3
import json

# Create a low-level client representing Amazon SageMaker Runtime
session = boto3.Session()
sagemaker_runtime = session.client('sagemaker-runtime', region_name=session.region_name)

# The name of the endpoint. The name must be unique within an AWS Region in your AWS account. 
endpoint_name='flan-t5-xxl-2023-03-10-07-09-14-864'

st.sidebar.title("Flan-T5 Parameters")

stop_word = st.sidebar.text_input("Stop word")
min_length, max_length = st.sidebar.slider("Min/Max length", 0, 200, (30, 100))
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.3)
rep_penalty = st.sidebar.slider("Repetition Penalty", min_value=0.9, max_value=1.2, value=1.0)

def generate_text(prompt):
    do_sample = temperature > 0
    payload = {
        "inputs": prompt,
        "min_length": min_length,
        "max_length": max_length,
        "temperature": temperature,
        "repetition_penalty": rep_penalty,
        "do_sample": do_sample,
    }

    response = sagemaker_runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='application/json',
        Body=json.dumps(payload)
    )

    result = json.loads(response['Body'].read().decode())
    return result


st.header("Flan-T5-XXL Playground")
prompt = st.text_area("Enter your prompt here:")

if st.button("Run"):
    generated_text = generate_text(prompt)
    if len(stop_word) > 0:
        generated_text = generated_text[:generated_text.rfind(stop_word)]
    st.write(generated_text)