import requests

excelFilePath = "data//users.xlsx"
url = "http://127.0.0.1:5000/upload-excel"

try:
    with open(excelFilePath, 'rb') as file:
        files = { 'file': file}
        response = requests.post(url, files=files)

    print(response.json())

except Exception as e:
    print('\n', e)