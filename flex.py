import http.client
import json

conn = http.client.HTTPSConnection("flexstudent.nu.edu.pk")

headersList = {
 "Accept": "*/*",
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
 "Cookie": "ASP.NET_SessionId=olqoh3sa25wegwk42tca152s;",
 "Content-Type": "application/json" 
}

Courses = {
    "NTC": 1896,
    "InfoSec": 1472,
    "CNet": 1470,
    "DAA": 1496,
    "DS": 1463,
    "CNet-lab": 1471,
    "DS-lab": 1464
}

payload = json.dumps({
  "CourseId": Courses["NTC"],
  "SemID": "20223"
})

conn.request("POST", "/Student/GetClassAvg", payload, headersList)
response = conn.getresponse()
result = response.read()

print(result.decode("utf-8"))