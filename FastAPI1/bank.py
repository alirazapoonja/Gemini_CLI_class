from fastapi import FastAPI, HTTPException

app = FastAPI()

users = {
    "saba": {"pin": 5617, "balance": 10000},
    "Ayesha": {"pin": 2222, "balance": 5000},
    "wania": {"pin": 4444, "balance": 20000}
}

@app.get("/")
def read_root():
    return {"message": "Bank API running"}

@app.post("/authenticate")
def authenticate_user(name: str, pin_number: int):
    user = users.get(name)
    if not user or user["pin"] != pin_number:
        raise HTTPException(status_code=401, detail={"error": "Invalid Credentials"})
    return {"name": name, "bank_balance": user["balance"]}

@app.post("/deposit")
def deposit_funds(name: str, amount: float):
    user = users.get(name)
    if not user:
        raise HTTPException(status_code=404, detail={"error": "User not found"})
    user["balance"] += amount
    return {"name": name, "bank_balance": user["balance"]}

@app.post("/bank-transfer")
def bank_transfer(sender_name: str, sender_pin: int, recipient_name: str, amount: float):
    sender = users.get(sender_name)
    if not sender or sender["pin"] != sender_pin:
        raise HTTPException(status_code=401, detail={"error": "Invalid Credentials"})

    if sender["balance"] < amount:
        raise HTTPException(status_code=400, detail={"error": "Insufficient balance"})

    recipient = users.get(recipient_name)
    if not recipient:
        raise HTTPException(status_code=404, detail={"error": "Recipient not found"})

    sender["balance"] -= amount
    recipient["balance"] += amount

    return {
        "message": "Transfer successful",
        "sender_updated_balance": sender["balance"],
        "recipient_updated_balance": recipient["balance"]
    }
