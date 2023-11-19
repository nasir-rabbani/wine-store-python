from fastapi import FastAPI
import psycopg2
import os
from typing import List
from pydantic import BaseModel

app = FastAPI()

# Pydantic models
class RecommendationRequest(BaseModel):
    user_id: str

class Recommendation(BaseModel):
    product_id: str
    recommendation_score: float

# Database configuration for Redshift
conn = psycopg2.connect(
    dbname=os.getenv("REDSHIFT_DB"),
    user=os.getenv("REDSHIFT_USER"),
    password=os.getenv("REDSHIFT_PASSWORD"),
    host=os.getenv("REDSHIFT_HOST"),
    port=os.getenv("REDSHIFT_PORT")
)
cur = conn.cursor()

@app.get("/recommendations/{user_id}", response_model=List[Recommendation])
async def get_recommendations(user_id: str):
    # Query Redshift for recommendations
    cur.execute("SELECT product_id, recommendation_score FROM recommendations WHERE user_id = %s", (user_id,))
    rows = cur.fetchall()
    return [Recommendation(product_id=row[0], recommendation_score=row[1]) for row in rows]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
