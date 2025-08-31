from fastapi import FastAPI,HTTPException
import uuid

app=FastAPI()
tokens={}
MAX_TOKENS=75
@app.get("/generate_link")
def generate_link():
    """Generate a temporary demo link with only quota."""
    token=str(uuid.uuid4())
    tokens[token]={
        "used":0,
        "max":MAX_TOKENS
    }
    return {"token":token}
@app.post("/ask")
def ask(token:str,question:str,tokens_used:int):
    if token not in tokens:
        raise HTTPException(status_code=400,detail="Invalid or expired token")
    remaining=tokens[token]["max"]-tokens[token]["used"]
    if remaining<=0:
        raise HTTPException(status_code=403,detail="Quota exceeded")
    if tokens_used>remaining:
        raise HTTPException(status_code=403,detail="Token quota will be exceeded with this query")
    tokens[token]["used"]+=tokens_used
    remaining=tokens[token]["max"]-tokens[token]["used"]
    return {
        "answer":f"Demo answer for: {question}",
        "remaining":remaining
    }