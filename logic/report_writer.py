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

def generate_daily_report(collected_bins):
    # Create a readable log for the AI
    log_text = ""
    for bin_data in collected_bins:
        log_text += f"- Bin ID: {bin_data['Bin ID']}, Fill: {bin_data['Fill Level']}%, Type: {bin_data['Waste Type']}, Urgency: {bin_data['Urgency Score']}\n"

    prompt = f"""
You are a waste operations supervisor.

Below is today's collection log. Please write a professional daily summary (100–150 words) including:
- Total number of bins collected
- Number of high urgency bins (Urgency > 70)
- Most common waste types
- Whether any hazardous bins were collected

Important:
- Only use the data shown below. Do NOT include data from previous days.
- Do NOT invent or assume bin IDs or stats not listed.

Collection Log:
{log_text}
"""


    credentials = get_credentials()
    model = ModelInference(
        model_id=os.getenv("MODEL_ID"),
        params={GenParams.MAX_NEW_TOKENS: 200},
        credentials=credentials,
        project_id=os.getenv("PROJECT_ID")
    )

    result = model.generate_text(prompt=prompt)
    return result.strip()
