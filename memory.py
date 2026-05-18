import os
import json
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# ━━━ Initialize Supabase ━━━
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_session(results: dict):
    """Save a completed session to Supabase."""
    try:
        dept_data = {}
        for dept in ["engineering", "product", "marketing", "operations"]:
            if dept in results:
                dept_data[dept] = results[dept]
        supabase.table("sessions").insert({
            "timestamp": results.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "goal": results.get("goal", ""),
            "mode": results.get("mode", ""),
            "cto_plan": results.get("cto", ""),
            "cpo_plan": results.get("cpo", ""),
            "cmo_plan": results.get("cmo", ""),
            "coo_plan": results.get("coo", ""),
            "departments": dept_data
        }).execute()
        print("✅ Session saved to Supabase!")
    except Exception as e:
        print(f"⚠️ Memory save failed: {e}")

def get_all_sessions():
    """Get all past sessions."""
    try:
        response = supabase.table("sessions").select("*").order("timestamp", desc=True).execute()
        return response.data
    except Exception as e:
        print(f"⚠️ Memory fetch failed: {e}")
        return []

def get_recent_sessions(limit=2):
    """Get most recent sessions."""
    try:
        response = supabase.table("sessions").select("timestamp, goal, cto_plan, cpo_plan, cmo_plan, coo_plan").order("timestamp", desc=True).limit(limit).execute()
        return response.data
    except Exception as e:
        print(f"⚠️ Memory fetch failed: {e}")
        return []

def build_memory_context(limit=2):
    """Build memory string to inject into agent tasks."""
    sessions = get_recent_sessions(limit)
    if not sessions:
        return ""
    context = "\n\n📚 COMPANY MEMORY — Previous Decisions:\n"
    context += "="*50 + "\n"
    for i, row in enumerate(sessions):
        context += f"\n[Session {i+1} — {row['timestamp']}]\n"
        context += f"Goal: {row['goal']}\n"
        context += f"CTO decided: {row['cto_plan'][:300]}...\n"
        context += f"CPO decided: {row['cpo_plan'][:300]}...\n"
        context += "-"*30 + "\n"
    context += "\nUse the above history to maintain consistency.\n"
    return context

def get_session_count():
    """Get total number of sessions."""
    try:
        response = supabase.table("sessions").select("id", count="exact").execute()
        return response.count or 0
    except Exception as e:
        print(f"⚠️ Count failed: {e}")
        return 0

def save_company_fact(key: str, value: str):
    """Save a persistent company fact."""
    try:
        supabase.table("company_facts").upsert({
            "key": key,
            "value": value,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }).execute()
    except Exception as e:
        print(f"⚠️ Fact save failed: {e}")

def get_company_facts():
    """Get all company facts."""
    try:
        response = supabase.table("company_facts").select("*").order("updated_at", desc=True).execute()
        return response.data
    except Exception as e:
        print(f"⚠️ Facts fetch failed: {e}")
        return []

def delete_all_memory():
    """Wipe all memory."""
    try:
        supabase.table("sessions").delete().neq("id", 0).execute()
        supabase.table("company_facts").delete().neq("id", 0).execute()
        print("✅ Memory cleared!")
    except Exception as e:
        print(f"⚠️ Memory clear failed: {e}")

print("✅ Supabase memory system initialized!")