import requests

try:
    response = requests.post('http://localhost:3000/api/campaigns/e5910d23-0b65-45c7-b10d-2d9765ee01dd/start?use_llm=true')
    print(f'Status Code: {response.status_code}')
    print(f'Response: {response.text}')
except Exception as e:
    print(f'Error: {e}')