import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = "postgresql+psycopg2://Mitya:Baburin17!@127.0.0.1:5432/database"
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
API_URL = "https://analitika.woysa.club/images/panel/json/download/niches.php?skip=0&price_min=0&price_max=1060225&up_vy_min=0&up_vy_max=108682515&up_vy_pr_min=0&up_vy_pr_max=2900&sum_min=1000&sum_max=82432725&feedbacks_min=0&feedbacks_max=32767&trend=false&sort=sum_sale&sort_dir=-1&id_cat=10000"