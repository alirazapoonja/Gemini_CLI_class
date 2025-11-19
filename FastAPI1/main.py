from fastapi import FastAPI

app = FastAPI()

bank_balance = 10000
@app.get("/authenticate")
async def root():
    return f"I am learning FASTAPI!!!{bank_balance}"

@app.get("/balance")
async def get_balance():
    return {"balance": bank_balance}

@app.post("/deposit/{amount}")
async def deposit(amount: int):
    global bank_balance
    bank_balance += amount
    return {"new_balance": bank_balance}

@app.post("/withdraw/{amount}")
async def withdraw(amount: int):
    global bank_balance
    if amount > bank_balance:
        return {"error": "Insufficient funds"}
    bank_balance -= amount
    return {"new_balance": bank_balance}    

@app.get("/status")
async def status():
    return {"status": "API is running"} 
@app.get("/")

async def home():
    return {"message": "Welcome to the Banking API"}

@app.get("/help")
async def help():
    return {
        "endpoints": {
            "/authenticate": "Authenticate the user",
            "/balance": "Get current bank balance",
            "/deposit/{amount}": "Deposit amount to bank balance",
            "/withdraw/{amount}": "Withdraw amount from bank balance",
            "/status": "Check API status",
            "/": "Home endpoint",
            "/help": "Get help information"
        }
    }
@app.get("/info")
async def info():
    return {
        "app_name": "Banking API",
        "version": "1.0.0",
        "description": "A simple banking API using FastAPI"
    }
@app.get("/contact")
async def contact():
    return {
           "email": "support@example.com",
           "phone": "+1-800-123-4567"
    }
