import sys
import os
# Add backend to path
sys.path.append(os.getcwd())

from app.database import SessionLocal, engine, Base
from app import models

# Verify connection and model
print("Creating database session...")
db = SessionLocal()

print("Creating test record...")
test_record = models.Detection(
    filename="test_orm_insert.jpg",
    original_file_url="http://orm.test/orig",
    processed_file_url="http://orm.test/proc",
    helmet_detected="YES",
    number_plate_detected="NO",
    plate_number="ORM-TEST"
)

try:
    db.add(test_record)
    db.commit()
    db.refresh(test_record)
    print(f"✅ Success! Record inserted with ID: {test_record.id}")
except Exception as e:
    print(f"❌ Error inserting record: {e}")
finally:
    db.close()
