import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GAMMA_API_KEY")

if key:
    print(f"Key found. Length: {len(key)}")
    print(f"Starts with: {key[:10]}...")
else:
    print("Key NOT found in environment.")
