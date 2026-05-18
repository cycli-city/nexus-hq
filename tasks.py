from crewai import Task
from agents import cto, cpo, cmo, coo

def create_tasks(goal, memory_context=""):
    """Create C-Suite tasks with optional memory context."""

    # Inject memory into each task if available
    memory_note = f"\n\n{memory_context}" if memory_context else ""

    cto_task = Task(
        description=f"Based on this company goal: '{goal}', define the tech stack, infrastructure plan and key technical milestones for the first 30 days.{memory_note}",
        expected_output="A clear technical plan with tech stack choices, architecture overview and 30-day engineering milestones.",
        agent=cto
    )
    cpo_task = Task(
        description=f"Based on this company goal: '{goal}', define the core features for MVP, user stories and product priorities for first 30 days.{memory_note}",
        expected_output="A product roadmap with MVP features, user stories and prioritized backlog for 30 days.",
        agent=cpo
    )
    cmo_task = Task(
        description=f"Based on this company goal: '{goal}', create a marketing plan to get first 100 users in 30 days.{memory_note}",
        expected_output="A 30-day marketing plan with channels, campaigns and user acquisition targets.",
        agent=cmo
    )
    coo_task = Task(
        description=f"Based on this company goal: '{goal}', create an operations plan, set team processes and define success metrics for 30 days.{memory_note}",
        expected_output="An operations plan with team workflows, budget overview and KPIs for 30 days.",
        agent=coo
    )
    return cto_task, cpo_task, cmo_task, coo_task