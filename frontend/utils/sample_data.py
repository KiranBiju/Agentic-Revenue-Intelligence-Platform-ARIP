import random

sample_leads = []

first_names = [
    "John", "Alice", "David", "Emma", "Michael",
    "Sophia", "Daniel", "Olivia", "James", "Ava"
]

last_names = [
    "Smith", "Johnson", "Brown", "Williams",
    "Jones", "Miller", "Davis", "Wilson"
]

for i in range(1, 1001):

    full_name = (
        f"{random.choice(first_names)} "
        f"{random.choice(last_names)}"
    )

    sample_leads.append({
        "user_id": i,
        "name": full_name,
        "years_experience": random.randint(0, 10),
        "company_size": random.randint(1, 500),
        "role_score": random.randint(1, 10),
        "activity_score": random.randint(1, 10),
        "responded": random.randint(0, 1)
    })