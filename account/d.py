import requests
import json


url = "https://live-server-8505.wati.io/api/v1/sendTemplateMessage?whatsappNumber=91"

payload = {
    "template_name": "new_chat_v1",
    "broadcast_name": "my_broadcast",
    "parameters": [
        {
            "name": "name",
            "value": "John"
        },
        {
            "name": "ordernumber",
            "value": "12345"
        }
    ]
}



headers = {
    "Content-Type": "application/json-patch+json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI1OTljODIwNS01ZTU2LTRmMzgtOWJmZi1jMzA4MjY4YmYxMjMiLCJ1bmlxdWVfbmFtZSI6InBuaHJpbW1pdWFlQGdtYWlsLmNvbSIsIm5hbWVpZCI6InBuaHJpbW1pdWFlQGdtYWlsLmNvbSIsImVtYWlsIjoicG5ocmltbWl1YWVAZ21haWwuY29tIiwiYXV0aF90aW1lIjoiMDMvMzAvMjAyMiAwODo1MToyNCIsImRiX25hbWUiOiI4NTA1IiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiQURNSU5JU1RSQVRPUiIsImV4cCI6MjUzNDAyMzAwODAwLCJpc3MiOiJDbGFyZV9BSSIsImF1ZCI6IkNsYXJlX0FJIn0.VzvpfwnowdE3QLBc1wfgNhPQ8JYrh2FM-xd6zJtC7QU"
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

print(response.text)