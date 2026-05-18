from llm_config import groq_llm

response = groq_llm.call("Say hello as if you are a CTO of a SaaS company.")
print(response)