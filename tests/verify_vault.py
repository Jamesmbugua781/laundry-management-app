import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def test_vault():
    print("--- Starting Vault Verification ---")
    
    # 1. Register Users (Assuming they don't exist, ignore error if they do)
    print("\n[1] Registering Users...")
    
    # We need an admin to register others, or just register them directly if endpoint allows (currently it needs admin)
    # Let's check users/routes.py: register_user needs RoleChecker(["admin"])
    # This means I need to create the first admin manually or change the route temporarily.
    
    # For the purpose of this test, I'll bypass the admin check by creating a script that uses the DB directly
    # OR I can temporarily make the registration public.
    
    print("Skipping direct registration due to admin restriction. Please use the script below to seed the DB.")

def seed_db():
    from app.core.database import SessionLocal
    from app.apps.users.models import User, UserRole
    from app.apps.orders.models import Order
    from app.core.security import hash_password
    
    db = SessionLocal()
    try:
        # Create Student
        student = db.query(User).filter(User.email == "student@example.com").first()
        if not student:
            student = User(
                email="student@example.com",
                hashed_password=hash_password("student123"),
                role=UserRole.STUDENT
            )
            db.add(student)
            print("Student created.")
        
        # Create Staff
        staff = db.query(User).filter(User.email == "staff@example.com").first()
        if not staff:
            staff = User(
                email="staff@example.com",
                hashed_password=hash_password("staff123"),
                role=UserRole.STAFF
            )
            db.add(staff)
            print("Staff created.")
            
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
    
    seed_db()
    
    # Now run the API test
    print("\n--- Testing API ---")
    
    # Login as Student
    print("Logging in as student...")
    resp = requests.post(f"{BASE_URL}/auth/login", data={"username": "student@example.com", "password": "student123"})
    student_token = resp.json().get("access_token")
    student_headers = {"Authorization": f"Bearer {student_token}"}
    
    # Create Order
    print("Creating order as student...")
    resp = requests.post(f"{BASE_URL}/orders/", json={"description": "Blue Jeans", "amount": 250.0}, headers=student_headers)
    order = resp.json()
    order_id = order.get("id")
    print(f"Order created: ID {order_id}")
    
    # Try to Mark as Paid (Should Fail)
    print("Attempting to mark as paid as student (Expect 403)...")
    resp = requests.patch(f"{BASE_URL}/orders/{order_id}/mark-as-paid", headers=student_headers)
    print(f"Status Code: {resp.status_code} (Expected 403)")
    
    # Login as Staff
    print("\nLogging in as staff...")
    resp = requests.post(f"{BASE_URL}/auth/login", data={"username": "staff@example.com", "password": "staff123"})
    staff_token = resp.json().get("access_token")
    staff_headers = {"Authorization": f"Bearer {staff_token}"}
    
    # Mark as Paid (Should Succeed)
    print("Attempting to mark as paid as staff (Expect 200)...")
    resp = requests.patch(f"{BASE_URL}/orders/{order_id}/mark-as-paid", headers=staff_headers)
    print(f"Status Code: {resp.status_code} (Expected 200)")
    print(f"Response: {resp.json()}")
    
    print("\n--- Vault Verification Complete ---")
