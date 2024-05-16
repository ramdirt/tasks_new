from dotenv import load_dotenv
import os

bind = "0.0.0.0:8000"
workers = 4

environment = os.getenv("ENVIRONMENT")

env = os.path.join(os.getcwd(), f".{environment}.env")

if os.path.exists(env):
    load_dotenv(env)