from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenAI
from langsmith import LangSmith

# Initialize LangSmith (automatically picks up API key from env vars)
tracing = LangSmith()

# Define a simple LLM Chain
prompt_template = "What is the capital of {country}?"
llm = OpenAI(model="gpt-4")
prompt = PromptTemplate.from_template(prompt_template)
chain = LLMChain(llm=llm, prompt=prompt)

# Run the chain with tracing enabled
result = tracing.trace(chain.invoke({"country": "France"}))

print(f"Result: {result}")
