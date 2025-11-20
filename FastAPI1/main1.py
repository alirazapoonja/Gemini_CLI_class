from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Complete Banking API")

# ----- DATABASE (In-Memory) -----
users = {
    "ali": {"pin": "1234", "balance": 5000},
    "ahmed": {"pin": "2222", "balance": 3000},
    "umar": {"pin": "9999", "balance": 10000}
}

# ----- REQUEST MODELS -----

class AuthRequest(BaseModel):
    name: str
    pin_number: str = Field(..., min_length=4, max_length=4)


class TransferRequest(BaseModel):
    sender_name: str
    sender_pin: str = Field(..., min_length=4, max_length=4)
    recipient_name: str
    amount: float = Field(..., gt=0)


# ----- ROUTES -----

@app.post("/authenticate")
def authenticate(req: AuthRequest):
    """Authenticate user using name + pin_number."""
    user = users.get(req.name)

    if not user or user["pin"] != req.pin_number:
        raise HTTPException(status_code=401, detail="Invalid name or PIN.")

    return {
        "message": "Authentication successful",
        "name": req.name,
        "balance": user["balance"]
    }


@app.get("/balance/{name}")
def get_balance(name: str):
    """Check balance of any user."""
    user = users.get(name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return {"name": name, "balance": user["balance"]}


@app.post("/deposit/{name}/{amount}")
def deposit(name: str, amount: float):
    """Deposit amount into the user's balance."""
    user = users.get(name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    users[name]["balance"] += amount

    return {
        "message": "Deposit successful",
        "name": name,
        "new_balance": users[name]["balance"]
    }


@app.post("/withdraw/{name}/{amount}")
def withdraw(name: str, amount: float):
    """Withdraw money from balance."""
    user = users.get(name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if amount > user["balance"]:
        raise HTTPException(status_code=400, detail="Insufficient funds.")

    users[name]["balance"] -= amount

    return {
        "message": "Withdraw successful",
        "name": name,
        "new_balance": users[name]["balance"]
    }


@app.post("/bank-transfer")
def bank_transfer(req: TransferRequest):
    """Transfer amount between sender & recipient + Re-authenticate recipient."""
    sender = users.get(req.sender_name)
    receiver = users.get(req.recipient_name)

    if not sender:
        raise HTTPException(status_code=404, detail="Sender not found.")
    if not receiver:
        raise HTTPException(status_code=404, detail="Recipient not found.")

    # authenticate sender
    if sender["pin"] != req.sender_pin:
        raise HTTPException(status_code=401, detail="Invalid sender PIN.")

    # check balance
    if sender["balance"] < req.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds.")

    # transfer money
    sender["balance"] -= req.amount
    receiver["balance"] += req.amount

    # authenticate receiver automatically
    receiver_auth = {
        "message": "Transfer completed!",
        "receiver_authenticated": True,
        "receiver_name": req.recipient_name,
        "receiver_new_balance": receiver["balance"]
    }

    return {
        "transfer_status": "Success",
        "sender_name": req.sender_name,
        "sender_balance": sender["balance"],
        "receiver_info": receiver_auth
    }

