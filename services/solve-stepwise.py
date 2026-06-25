@app.post("/solve-stepwise")
async def solve_stepwise(payload: SolveRequest):
    engine = get_engine(payload.engine)
    prompt = f"Solve this math problem step-by-step:\n{payload.question}"
    result = await engine.generate(prompt)
    return {"solution": result}
