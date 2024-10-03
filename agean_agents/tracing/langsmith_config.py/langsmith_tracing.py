from langchain_core.runnables import RunnableParallel
from langsmith import RunnableConfig
from langchain.chains import chain
from langsmith import tracing 

import os

if os.getenv("ENABLE_TRACING") == "true":
    tracing_enabled = True
else:
    tracing_enabled = False

# Use LangSmith tracing only when enabled
if tracing_enabled:
    result = tracing.trace(chain.invoke({"input_data": data}))
else:
    result = chain.invoke({"input_data": data})

'''
# Define multiple chains or agents
chain1 = LLMChain(llm=llm, prompt=PromptTemplate.from_template("What is the largest city in {country}?"))
chain2 = LLMChain(llm=llm, prompt=PromptTemplate.from_template("What language is spoken in {country}?"))

# Combine them in a parallel workflow
combined_workflow = RunnableParallel({
    "city": chain1,
    "language": chain2
})

# Run the combined workflow with tracing
result = tracing.trace(combined_workflow.invoke({"country": "France"}))
print(result)



# Create a configuration with custom tags
config = RunnableConfig(tags=["testing", "v1"])

# Run a chain with custom tags
result = chain.invoke({"country": "Germany"}, config=config)
config = RunnableConfig(tags=["production", "financial-analysis"])
result = chain.invoke({"input_data": data}, config=config)
'''