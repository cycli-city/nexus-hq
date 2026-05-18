from crewai import Task
from department_agents import (
    backend_dev, frontend_dev, devops_engineer, qa_engineer,
    product_manager, ux_designer, data_analyst,
    content_writer, seo_specialist, social_media_manager, paid_ads_specialist,
    sales_rep, customer_support, finance_agent, hr_agent
)

def create_department_tasks(goal, cto_plan, cpo_plan, cmo_plan, coo_plan):
    """Department agents execute based on C-Suite plans."""

    # 🔧 ENGINEERING TEAM (under CTO)
    backend_task = Task(
        description=f"Based on CTO's plan: '{cto_plan[:1500]}', design the backend architecture, APIs, and database schema for: '{goal}'.",
        expected_output="Backend technical specifications with API endpoints and database schema.",
        agent=backend_dev
    )
    frontend_task = Task(
        description=f"Based on CTO's plan: '{cto_plan[:1500]}', design the frontend UI components and pages for: '{goal}'.",
        expected_output="Frontend component list with page structure and key UI elements.",
        agent=frontend_dev
    )
    devops_task = Task(
        description=f"Based on CTO's plan: '{cto_plan[:1500]}', design the deployment pipeline and infrastructure for: '{goal}'.",
        expected_output="DevOps plan with CI/CD pipeline, hosting, and monitoring setup.",
        agent=devops_engineer
    )
    qa_task = Task(
        description=f"Based on CTO's plan: '{cto_plan[:1500]}', create a testing strategy for: '{goal}'.",
        expected_output="QA testing plan with test cases, tools, and automation strategy.",
        agent=qa_engineer
    )

    # 📦 PRODUCT TEAM (under CPO)
    pm_task = Task(
        description=f"Based on CPO's roadmap: '{cpo_plan[:1500]}', write detailed user stories and acceptance criteria for: '{goal}'.",
        expected_output="A list of 5-7 user stories with acceptance criteria.",
        agent=product_manager
    )
    ux_task = Task(
        description=f"Based on CPO's roadmap: '{cpo_plan[:1500]}', describe the UX flow and wireframe ideas for: '{goal}'.",
        expected_output="UX flow description and key wireframe concepts.",
        agent=ux_designer
    )
    data_task = Task(
        description=f"Based on CPO's roadmap: '{cpo_plan[:1500]}', define product KPIs and analytics events to track for: '{goal}'.",
        expected_output="List of product KPIs, analytics events, and dashboards to build.",
        agent=data_analyst
    )

    # 📣 MARKETING TEAM (under CMO)
    content_task = Task(
        description=f"Based on CMO's plan: '{cmo_plan[:1500]}', write a content marketing calendar with 5 blog post ideas for: '{goal}'.",
        expected_output="Content calendar with 5 blog post titles and brief outlines.",
        agent=content_writer
    )
    seo_task = Task(
        description=f"Based on CMO's plan: '{cmo_plan[:1500]}', create an SEO strategy with target keywords for: '{goal}'.",
        expected_output="SEO strategy with primary keywords, content topics, and link-building ideas.",
        agent=seo_specialist
    )
    social_task = Task(
        description=f"Based on CMO's plan: '{cmo_plan[:1500]}', design a social media strategy with 7 post ideas for: '{goal}'.",
        expected_output="Social media plan with platform strategy and 7 example posts.",
        agent=social_media_manager
    )
    ads_task = Task(
        description=f"Based on CMO's plan: '{cmo_plan[:1500]}', design a paid ads strategy with campaign ideas for: '{goal}'.",
        expected_output="Paid ads strategy with platforms, targeting, and 3 ad creative ideas.",
        agent=paid_ads_specialist
    )

    # ⚙️ OPERATIONS TEAM (under COO)
    sales_task = Task(
        description=f"Based on COO's plan: '{coo_plan[:1500]}', design a sales outreach playbook for: '{goal}'.",
        expected_output="Sales playbook with outreach scripts, target persona, and demo flow.",
        agent=sales_rep
    )
    support_task = Task(
        description=f"Based on COO's plan: '{coo_plan[:1500]}', design customer support processes for: '{goal}'.",
        expected_output="Support plan with channels, response SLAs, and common FAQs.",
        agent=customer_support
    )
    finance_task = Task(
        description=f"Based on COO's plan: '{coo_plan[:1500]}', create a 30-day budget breakdown for: '{goal}'.",
        expected_output="Detailed budget with line items, monthly run rate, and revenue projection.",
        agent=finance_agent
    )
    hr_task = Task(
        description=f"Based on COO's plan: '{coo_plan[:1500]}', design team onboarding and processes for: '{goal}'.",
        expected_output="HR plan with team structure, onboarding checklist, and weekly rituals.",
        agent=hr_agent
    )

    return {
        "engineering": [backend_task, frontend_task, devops_task, qa_task],
        "product": [pm_task, ux_task, data_task],
        "marketing": [content_task, seo_task, social_task, ads_task],
        "operations": [sales_task, support_task, finance_task, hr_task]
    }