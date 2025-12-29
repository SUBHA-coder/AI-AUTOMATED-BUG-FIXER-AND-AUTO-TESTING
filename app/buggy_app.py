def register_user(email, password, confirm_password):
    if not email or not password or not confirm_password:
        return {"status": "error", "message": "All fields are required"}
    
    if "@" not in email:
        return {"status": "error", "message": "Invalid email format"}
    
    if password != confirm_password:
        return {"status": "error", "message": "Passwords do not match"}
    
    return {"status": "success", "message": "User registered"}

def login_user(email, password):
    stored_email = "user@example.com"
    stored_password = "password123"
    
    if email != stored_email:
        return {"status": "error", "message": "Invalid email"}
    
    if password != stored_password:
        return {"status": "error", "message": "Invalid password"}
    
    return {"status": "success", "message": "Login successful"}

def calculate_discount(price, percentage):
    if price < 0 or percentage < 0 or percentage > 100:
        return 0
    
    discounted_price = price - (price * percentage / 100)
    return discounted_price

def withdraw_balance(balance, amount):
    if amount < 0:
        return {"status": "error", "message": "Invalid amount"}
    
    if amount > balance:
        return {"status": "error", "message": "Insufficient funds"}
    
    new_balance = balance - amount
    return {"status": "success", "new_balance": new_balance}