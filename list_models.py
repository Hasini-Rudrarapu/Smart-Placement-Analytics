from openai import OpenAI

print("Starting...")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

print("Connected")

models = client.models.list()

print("Models received:", len(models.data))

for model in models.data[:20]:
    print(model.id)