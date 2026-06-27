import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

load_dotenv()

project = AIProjectClient(
    endpoint = os.environ["PROJECT_ENDPOINT"],
    credential = DefaultAzureCredential(),
)

client = project.get_openai_client()

response = client.responses.create(
    model = "gpt-4.1-mini",
    input = [
        {"role": "System",
        "content": "You are a helpful travel advisor." " Use the following data to answer"+ retrieved_context},
        {"role": "user", "content": "What are the top 5 tourist attractions in Paris?"}
    ],
)

print(response.output_text)