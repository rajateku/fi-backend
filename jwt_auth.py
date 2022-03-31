import jwt
import read_write_db

key = "secret"

payload = {
  "id": {
    "S": "9000001"
  },
  "password": {
    "S": "roundpier"
  },
  "username": {
    "S": "roundpier"
  },
  "name": {
    "S": "roundpier"
  }
}

encoded = jwt.encode(payload, key, algorithm="HS256")
print(encoded)
decoded = jwt.decode(encoded, key, algorithms="HS256")

print(decoded)


def read_active_jwts(jwt):
    all_jwts = read_write_db.get_all_data(TableName="activeJWTs")
    for jwts in all_jwts:
        if jwt == jwts["jwt"]:
            return "JWT exists"
    return "No active jwt"

def check_login(req):
    all_orgs = read_write_db.get_all_data(TableName="orgIds")
    for org in all_orgs:
        if org["username"] == req["username"] and org["password"] == req["password"]:
            print(org)
            encoded = jwt.encode(org, key, algorithm="HS256")
            read_write_db.create_review(TableName="activeJWTs", item={"jwt" : encoded})
            activeJWTs = read_active_jwts(encoded)
            print(activeJWTs)

            return {"jwt" : encoded}
    return {"jwt" : "user doesn't exist"}