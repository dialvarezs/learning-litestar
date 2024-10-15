from pwdlib import PasswordHash
import jwt
import time

# password_hasher = PasswordHash.recommended()
# hashed_password = password_hasher.hash("secret123")

# print(hashed_password)

# print(password_hasher.verify("secret1233", hashed_password))

seconds = time.time()
payload = {"name": "user1", "iat": seconds, "exp": seconds + 20, "nbf": seconds + 10}
token = jwt.encode(payload, "supersecret")
print(token)
# time.sleep(2)

print(jwt.decode(token, "supersecret", algorithms=["HS256"]))