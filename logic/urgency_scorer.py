import os
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from dotenv import load_dotenv

load_dotenv()

def get_credentials():
    return Credentials(
        api_key=os.getenv("API_KEY"),
        url="https://us-south.ml.cloud.ibm.com"
    )

def score_bin(bin_data):
    from re import findall

    prompt = f"""
As a public health and logistics expert, calculate an 'Urgency Score' from 1-100 for the following waste bin.
Prioritize hazardous waste above all else. Highly filled bins and bins with organic waste that haven't been collected for more than a day should also have high scores.
- Bin ID: {bin_data['Bin ID']}
- Fill Level: {bin_data['Fill Level']}%
- Waste Type: {bin_data['Waste Type']}
- Days Since Last Collection: {bin_data['Days Since Last Collection']}
Output only the numeric Urgency Score.
"""

    credentials = get_credentials()
    model = ModelInference(
        model_id=os.getenv("MODEL_ID"),
        params={GenParams.MAX_NEW_TOKENS: 20},
        credentials=credentials,
        project_id=os.getenv("PROJECT_ID")
    )
    
    print("📤 Prompt sent to Granite:\n", prompt)

    result = model.generate_text(prompt=prompt)



    numbers = findall(r"\d+", result)
    if numbers:
        return int(numbers[0]) 
    else:
        return 50  # Default score if no number found