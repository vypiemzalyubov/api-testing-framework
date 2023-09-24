import json

json_data = """{
  "detail": [
    {
      "loc": [
        "query",
        "status"
      ],
      "msg": "value is not a valid enumeration member; permitted: 'ACTIVE', 'BANKRUPT', 'CLOSED'",
      "type": "type_error.enum",
      "ctx": {
        "enum_values": [
          "ACTIVE",
          "BANKRUPT",
          "CLOSED"
        ]
      }
    }
  ]
}"""

data = json.loads(json_data)
# for item in data["detail"]:
#     print(item["msg"])
print(data["detail"][0]["msg"])