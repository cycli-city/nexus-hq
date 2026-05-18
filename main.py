from crewai import Crew, Process
from agents import cto, cpo, cmo, coo
from tasks import cto_task, cpo_task, cmo_task, coo_task
from datetime import datetime
import os

print("🏢 AI Company Starting Up...")
print("👤 CEO: You")
print("🤖 C-Suite: CTO, CPO, CMO, COO")
print("="*50)

# --- Assemble the Crew ---
company = Crew(
    agents=[cto, cpo, cmo, coo],
    tasks=[cto_task, cpo_task, cmo_task, coo_task],
    process=Process.sequential,
    verbose=True
)

# --- CEO fires the starting gun ---
print("\n🚀 CEO: Team, let's plan our first 30 days!")
result = company.kickoff()

# --- Auto-save outputs ---
os.makedirs("outputs", exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Save each agent's output
tasks_results = {
    "CTO_Technical_Plan": cto_task.output.raw,
    "CPO_Product_Roadmap": cpo_task.output.raw,
    "CMO_Marketing_Plan": cmo_task.output.raw,
    "COO_Operations_Plan": coo_task.output.raw,
}

for name, content in tasks_results.items():
    filename = f"outputs/{timestamp}_{name}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {name.replace('_', ' ')}\n\n")
        f.write(content)
    print(f"✅ Saved: {filename}")

print("\n📁 All plans saved to /outputs folder!")