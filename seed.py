# seed.py
"""
Seed script to populate database with test data.
Run this to reset your database with fresh test data.
"""
from datetime import time  
from database import SessionLocal, engine, Base
from models.user import User
from models.member import Member
from models.dining_room import DiningRoom
from models.time_slot import TimeSlot


def seed_database():
    """
    Drop all tables, recreate them, and add seed data.
    WARNING: This deletes ALL data!
    """
    print("🗑️  Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("🔨 Creating all tables...")
    Base.metadata.create_all(bind=engine)
    
    print("🌱 Seeding data...")
    
    db = SessionLocal()
    
    try:
        # ============================================================
        # USER 1: Josh
        # ============================================================
        josh_user = User(
            email="josh@josh.com",
            name="Josh",
            is_admin=False
        )
        josh_user.set_password("1111")
        db.add(josh_user)
        db.commit()
        db.refresh(josh_user)
        print(f"✅ Created user: {josh_user.email}")
        
        # Member: Josh (self)
        josh_member = Member(
            user_id=josh_user.id,
            name="Josh",
            relation="self",
            dietary_restrictions="no shellfish"
        )
        db.add(josh_member)
        print(f"   └─ Member: {josh_member.name} ({josh_member.relation})")
        
        # Member: Dorrie (spouse)
        dorrie_member = Member(
            user_id=josh_user.id,
            name="Dorrie",
            relation="spouse",
            dietary_restrictions="no bluecheese"
        )
        db.add(dorrie_member)
        print(f"   └─ Member: {dorrie_member.name} ({dorrie_member.relation})")
        
        
        # ============================================================
        # USER 2: Sarah
        # ============================================================
        sarah_user = User(
            email="sarah@sarah.com",
            name="Sarah",
            is_admin=False
        )
        sarah_user.set_password("1111")
        db.add(sarah_user)
        db.commit()
        db.refresh(sarah_user)
        print(f"✅ Created user: {sarah_user.email}")
        
        # Member: Sarah (self)
        sarah_member = Member(
            user_id=sarah_user.id,
            name="Sarah",
            relation="self",
            dietary_restrictions="no bananas"
        )
        db.add(sarah_member)
        print(f"   └─ Member: {sarah_member.name} ({sarah_member.relation})")
        
        # Member: Reed (spouse/partner)
        reed_member = Member(
            user_id=sarah_user.id,
            name="Reed",
            relation="spouse",
            dietary_restrictions=None
        )
        db.add(reed_member)
        print(f"   └─ Member: {reed_member.name} ({reed_member.relation})")
        
        db.commit()
        
        # ============================================================
        # DINING ROOMS (Infrastructure)
        # ============================================================
        print("\n🏛️  Creating dining rooms...")
        
        dining_rooms = [
            {"name": "Main Hall", "capacity": 100},
            {"name": "Garden Room", "capacity": 50},
            {"name": "Private Dining", "capacity": 20},
            {"name": "Terrace", "capacity": 30},
            {"name": "Wine Cellar", "capacity": 15},
        ]
        
        for room_data in dining_rooms:
            room = DiningRoom(
                name=room_data["name"],
                capacity=room_data["capacity"]
            )
            db.add(room)
            print(f"   └─ {room.name} (capacity: {room.capacity})")
        
        db.commit()

        # ============================================================
        # TIME SLOTS (Infrastructure)
        # ============================================================
        print("\n🕐 Creating time slots...")
        
        time_slots = [
            {"name": "Breakfast", "start_time": time(8, 0), "end_time": time(11, 0)},
            {"name": "Lunch", "start_time": time(12, 0), "end_time": time(15, 0)},
            {"name": "Dinner", "start_time": time(18, 0), "end_time": time(21, 0)},
            {"name": "Late Night", "start_time": time(21, 0), "end_time": time(23, 30)},
        ]
        
        for slot_data in time_slots:
            slot = TimeSlot(
                name=slot_data["name"],
                start_time=slot_data["start_time"],
                end_time=slot_data["end_time"]
            )
            db.add(slot)
            print(f"   └─ {slot.name} ({slot.start_time.strftime('%I:%M %p')} - {slot.end_time.strftime('%I:%M %p')})")
        
        db.commit()
        
        # ============================================================
        # SUCCESS MESSAGE (moved to end)
        # ============================================================
        print("\n" + "="*50)
        print("🎉 Database seeded successfully!")
        print("="*50)
        print("\n📧 Login credentials:")
        print("   Josh:  josh@josh.com / 1111")
        print("   Sarah: sarah@sarah.com / 1111")
        print("\n")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    # Confirm before destroying data
    response = input("⚠️  This will DELETE all data. Continue? (yes/no): ")
    if response.lower() == "yes":
        seed_database()
    else:
        print("❌ Seed cancelled.")