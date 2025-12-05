from database import SessionLocal, engine
import models

# Reset DB
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

advisors = [
    {
        "name": "Dr. Sarah Chen",
        "department": "Computer Science",
        "research_areas": "Artificial Intelligence, Machine Learning, Neural Networks, Computer Vision",
        "bio": "Expert in deep learning. I run the Vision Lab.",
        "mentoring_style": "Hands-off, expects independence"
    },
    {
        "name": "Dr. James Miller",
        "department": "Computer Science",
        "research_areas": "Human Computer Interaction, UX, Accessibility, Frontend",
        "bio": "Focused on making tech accessible for everyone.",
        "mentoring_style": "Collaborative, meets weekly"
    },
    {
        "name": "Dr. Emily Zhang",
        "department": "Data Science",
        "research_areas": "Natural Language Processing, NLP, Linguistics, Chatbots",
        "bio": "Building the next generation of LLMs.",
        "mentoring_style": "Research-focused, rigorous"
    },
    {
        "name": "Dr. Robert Lang",
        "department": "Electrical Engineering",
        "research_areas": "Robotics, Control Systems, Automation, Hardware",
        "bio": "Working on autonomous drones.",
        "mentoring_style": "Hands-on, lab-based"
    }
]

print("Seeding Advisors...")
for adv in advisors:
    db_adv = models.Advisor(**adv)
    db.add(db_adv)

db.commit()
print("Done!")
db.close()
