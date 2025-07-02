from app.database import SessionLocal
from app.models import User
from app.auth import hash_password

db = SessionLocal()
user = User(email="ops@example.com", password_hash=hash_password("opspassword"), role="ops", is_verified=True)
db.add(user)
db.commit()
db.close()
print("Ops user created!")
