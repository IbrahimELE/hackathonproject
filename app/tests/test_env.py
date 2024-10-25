from dotenv import load_dotenv
import os

load_dotenv()

print("SECRET_KEY:", os.getenv("SECRET_KEY"))
print("ALGORITHM:", os.getenv("ALGORITHM"))
print("ACCESS_TOKEN_EXPIRE_MINUTES:", os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
print("DATABASE_URL:", os.getenv("DATABASE_URL"))
