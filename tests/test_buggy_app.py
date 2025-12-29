import sys
import os
import pytest

# Add the parent directory to sys.path to import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.buggy_app import register_user, login_user, calculate_discount, withdraw_balance

def test_register_user_invalid_email():
    """Test registration with invalid email format (missing @)."""
    result = register_user("invalid-email", "password123", "password123")
    # Expectation: Should fail validation
    assert result["status"] == "error", "Should reject invalid email format"

def test_login_user_wrong_password():
    """Test login with correct email but wrong password."""
    result = login_user("user@example.com", "wrongpassword")
    # Expectation: Should fail login
    assert result["status"] == "error", "Should fail login with wrong password"

def test_calculate_discount_logic():
    """Test discount calculation logic."""
    # Price 200, 50% discount -> Should be 100
    result = calculate_discount(200, 50)
    assert result == 100, f"Expected 100, got {result}"

def test_withdraw_balance_overdraft():
    """Test withdrawing more than available balance."""
    result = withdraw_balance(100, 200)
    # Expectation: Should fail due to insufficient funds
    assert result["status"] == "error", "Should fail withdrawal when amount > balance"
