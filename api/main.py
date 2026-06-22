from fastapi import FastAPI
from generate_questions import generate_questions_handler
from solve_stepwise import solve_stepwise_handler
from chapter_summary import chapter_summary_handler

app = FastAPI()

@app.post("/generate-questions")
async def generate_questions(payload: dict):
    return generate_questions_handler(payload)

@app.post("/solve-stepwise")
async def solve_stepwise(payload: dict):
    return solve_stepwise_handler(payload)

@app.post("/chapter-summary")
async def chapter_summary(payload: dict):
    return chapter_summary_handler(payload)
