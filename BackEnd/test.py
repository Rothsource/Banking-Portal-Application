from app import create_app, db
from app.controller.users import create_user

app = create_app()

# 🔹 Enter app context
with app.app_context():
    # Now you can safely use User.query or db.session
        user, error = create_user(
        username="alice",
        email="alice@example.com",
        password="password123",
        user_type="customer",  # ✅ allowed
        digits="123456",
        gov_id="GOV123"
    )
print(user, error)
