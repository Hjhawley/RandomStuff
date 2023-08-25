import openai

openai.api_key = 'sk-...Azjv'

response = openai.Completion.create(
    engine = 'text-davinci-003',
    prompt = 'Once upon a time',
    max_tokens = 50,
    temperature = 0.8,
    top_p = 0.5
)

print(response.choices[0].text)