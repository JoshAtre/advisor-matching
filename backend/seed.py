from database import SessionLocal, engine
import models

# WARNING: This resets the DB
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

advisors = [
    {
        "name": "Dr. Sarah Chen",
        "department": "Computer Science",
        "research_areas": "Artificial Intelligence, Machine Learning, Computer Vision",
        "bio": "I run the Vision Lab. Looking for students with strong math backgrounds.",
        "mentoring_style": "Hands-off",
        "image_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah"
    },
    {
        "name": "Dr. James Miller",
        "department": "Computer Science",
        "research_areas": "HCI, Frontend, UX Design, Accessibility",
        "bio": "Focused on making tech accessible. We build real-world apps.",
        "mentoring_style": "Collaborative",
        "image_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=James"
    },
    {
        "name": "Dr. Emily Zhang",
        "department": "Data Science",
        "research_areas": "NLP, Linguistics, Large Language Models",
        "bio": "Building the next generation of LLMs.",
        "mentoring_style": "Rigorous",
        "image_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Emily"
    },
    {
        "name": "Dr. Robert Lang",
        "department": "Electrical Engineering",
        "research_areas": "Robotics, Automation, Hardware Control",
        "bio": "Working on autonomous drones and swarms.",
        "mentoring_style": "Hands-on",
        "image_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Robert"
    }
]

print("Seeding Advisors...")
for adv in advisors:
    db.add(models.Advisor(**adv))

db.commit()
print("Database reset and seeded!")
db.close()
