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

def plan_route(scored_bins):
    bin_lines = ""
    for bin_data in scored_bins:
        bin_lines += f"- {bin_data['Bin ID']}, Urgency: {bin_data['Urgency Score']}\n"


    prompt = f"""
You are a smart waste management planner.

Your job:
- You are given a list of garbage bins and their urgency score.
- Sort them in the best order for collection.
- Visit the bins with higher urgency first.
- Return only a simple list of Bin IDs, separated by commas.
- Do not return any explanation or code.

Bins:
{bin_lines}
"""


    credentials = get_credentials()
    model = ModelInference(
        model_id=os.getenv("ROUTE_MODEL_ID", os.getenv("MODEL_ID")),
        params={GenParams.MAX_NEW_TOKENS: 100},
        credentials=credentials,
        project_id=os.getenv("PROJECT_ID")
    )

    result = model.generate_text(prompt=prompt)
    print("🧾 Raw AI response:\n", result)


    import re
    lines = re.findall(r'\bBIN-\d{3}\b', result)
    unique_bins = []
    for bin_id in lines:
        if bin_id not in unique_bins:
            unique_bins.append(bin_id)
    return unique_bins

