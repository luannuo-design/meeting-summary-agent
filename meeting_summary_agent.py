import anthropic

client = anthropic.Anthropic()
MODEL = "claude-opus-4-7"

# ---------- 3 sample meeting notes ----------

SAMPLES = {
    "1": {
        "title": "Product Roadmap Q3",
        "notes": """
Date: 2026-05-28
Attendees: Sarah (PM), James (Engineering Lead), Priya (Design), Tom (Marketing)

Sarah opened the meeting by reviewing Q2 results. Revenue hit 95% of target.

James confirmed the new search feature is on track for June 30 release. He needs two
extra engineers by June 10 to meet the deadline. He will send a staffing request to HR today.

Priya presented three new dashboard mockups. The team chose option B. Priya will share
final assets with James by June 5.

Tom raised concerns about the launch timeline clashing with a competitor announcement on
July 1. He will draft a revised launch plan and share it with Sarah by May 30.

Sarah will schedule a follow-up review for June 15 to check progress on all items.
        """,
    },
    "2": {
        "title": "Weekly Engineering Standup",
        "notes": """
Date: 2026-05-28
Attendees: James (Lead), Alice (Backend), Ben (Frontend), Carmen (QA)

Alice: Finished the payment API integration. Awaiting code review from James by end of day.
Ben: Login page redesign is 80% done. Will complete it tomorrow. Blocked on the colour
palette decision — needs Design sign-off.
Carmen: Found three critical bugs in the checkout flow. Will file detailed tickets in Jira today.
Ben will fix the two frontend bugs; Alice will handle the backend one, targeting Friday.
James will do Alice's code review today and will unblock Ben by pinging Priya for the
colour palette decision.
Next standup: Thursday 9 am.
        """,
    },
    "3": {
        "title": "Client Onboarding Kickoff — Acme Corp",
        "notes": """
Date: 2026-05-28
Attendees: Lisa (Account Manager), David (Solutions Engineer), Rachel (Acme Corp CTO)

Lisa welcomed Rachel and gave an overview of the onboarding process (6 weeks).

Rachel confirmed Acme's primary goal: migrate 10 000 user records from their legacy
system by June 30. She flagged that their IT team is small and will need hands-on support.

David will provide a data-migration checklist to Rachel by June 2 and will schedule a
technical deep-dive call with Acme's IT team for the week of June 9.

Lisa will set up Acme's account in the customer portal today and send Rachel login
credentials by close of business.

Rachel will share a sample data export (anonymised) with David by June 4 so David can
validate the migration scripts before the full run.

Next milestone check-in: June 16 at 2 pm.
        """,
    },
}

# ---------- helper: call Claude ----------

def ask_claude(prompt: str) -> str:
    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()

# ---------- agent steps ----------

def summarise(notes: str) -> str:
    print("\nSummarising the meeting...")
    return ask_claude(
        f"Summarise this meeting in 3-5 clear bullet points:\n\n{notes}"
    )

def extract_actions(notes: str) -> str:
    print("Extracting action items...")
    return ask_claude(
        f"List every action item from this meeting as a numbered list. "
        f"Be specific and include deadlines where mentioned:\n\n{notes}"
    )

def identify_owners(actions: str) -> str:
    print("Identifying owners...")
    return ask_claude(
        f"From these action items, create a table with columns: "
        f"Owner | Action | Deadline\n\n{actions}"
    )

def draft_email(title: str, summary: str, actions: str) -> str:
    print("Drafting follow-up email...")
    return ask_claude(
        f"Write a short, professional follow-up email for a meeting called '{title}'. "
        f"Include the summary and action items below. Keep it under 200 words.\n\n"
        f"SUMMARY:\n{summary}\n\nACTIONS:\n{actions}"
    )

# ---------- main flow ----------

def main():
    print("=" * 55)
    print("   Meeting Summary Agent")
    print("=" * 55)
    print("\nAvailable sample meetings:")
    for key, sample in SAMPLES.items():
        print(f"  {key}. {sample['title']}")

    choice = input("\nEnter 1, 2, or 3: ").strip()
    if choice not in SAMPLES:
        print("Invalid choice. Please run the script again and enter 1, 2, or 3.")
        return

    meeting = SAMPLES[choice]
    print(f"\nYou selected: {meeting['title']}")
    print("-" * 55)

    summary = summarise(meeting["notes"])
    print(f"\nSUMMARY\n{summary}")

    actions = extract_actions(meeting["notes"])
    print(f"\nACTION ITEMS\n{actions}")

    owners = identify_owners(actions)
    print(f"\nOWNERS TABLE\n{owners}")

    email = draft_email(meeting["title"], summary, actions)
    print(f"\nFOLLOW-UP EMAIL\n{email}")

    print("\n" + "=" * 55)
    print("Done!")

if __name__ == "__main__":
    main()
