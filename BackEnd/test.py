from app import create_app, db
from app.controller import user_login, verify_otp

app = create_app()

with app.app_context():
    user, error, role, get_otp = user_login(
        '13224345656771',
        'sr6024010023@camtech',
        'roth123pro'
    )

    if error:
        print("❌ Error:", error)
    else:
        print("✅ Login success")
        print("User ID:", user.id)
        print("Role:", role)

        if role != "customer":
            otp_in_db = user.otp
            print("Generated OTP in DB:", get_otp)

            # simulate user typing OTP
            # valid, err = verify_otp(user.id, otp_in_db)
            # print("Verify OTP result:", valid, err)
