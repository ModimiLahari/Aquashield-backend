from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("https://scpgmmxjmqsriepajwut.supabase.co")
SUPABASE_KEY = os.getenv("sb_publishable_-hwi0VcyntVSLs2qzYy8vw_gJoU1obC")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)