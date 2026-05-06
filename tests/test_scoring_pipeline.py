from app.schemas.lead import LeadInput
from app.orchestrator.orchestrator import DecisionOrchestrator


def generate_test_leads(n=30):
    return [
        LeadInput(
            user_id=i,
            name=f"User{i}",
            role="Founder" if i % 3 == 0 else "Engineer",
            activity_score=(i % 10) + 1,
            years_experience=(i % 7) + 1,
            company_size=(i % 5) * 50 + 50
        )
        for i in range(n)
    ]


if __name__ == "__main__":

    leads = generate_test_leads(30)

    orchestrator = DecisionOrchestrator()

    result = orchestrator.run_campaign(leads)

    print("\nFINAL RESULT:")
    print(result)

    print("\nTOP 5 SCORES:")
    for r in result["ranked_leads"]:
        print(r["priority_score"])

    print("\nFOUNDER CHECK:")
    for r in result["ranked_leads"]:
        if r["user_id"] % 3 == 0:
            print(r)