from typing import TypedDict
import re

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from langgraph.graph import StateGraph, START, END

from tools import calculator


load_dotenv()


class AgentState(TypedDict):
    question: str
    result: str
    used_tool: bool


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)


def extract_expression(question):
    pattern = r"(\d+(?:\.\d+)?)\s*([+\-*/])\s*(\d+(?:\.\d+)?)"

    match = re.search(pattern, question)

    if match:
        return (
            match.group(1)
            + match.group(2)
            + match.group(3)
        )

    return None


def decision_node(state):

    question = state["question"]

    expression = extract_expression(question)

    if expression:
        return {
            "result": expression,
            "used_tool": True
        }

    return {
        "result": "",
        "used_tool": False
    }


def calculator_node(state):

    expression = state["result"]

    result = calculator.invoke({
        "expression": expression
    })

    return {
        "result": result
    }


def answer_node(state):

    question = state["question"]

    if state["used_tool"]:

        return {
            "result": f"The calculator tool was used.\n\n{question}\nAnswer: {state['result']}"
        }

    response = llm.invoke([
        HumanMessage(content=question)
    ])

    return {
        "result": response.content
    }


def route_question(state):

    if state["used_tool"]:
        return "calculator"

    return "answer"


graph_builder = StateGraph(AgentState)


graph_builder.add_node("decision", decision_node)

graph_builder.add_node("calculator", calculator_node)

graph_builder.add_node("answer", answer_node)


graph_builder.add_edge(
    START,
    "decision"
)


graph_builder.add_conditional_edges(
    "decision",
    route_question,
    {
        "calculator": "calculator",
        "answer": "answer"
    }
)


graph_builder.add_edge(
    "calculator",
    "answer"
)


graph_builder.add_edge(
    "answer",
    END
)


graph = graph_builder.compile()


def run_agent(question):

    result = graph.invoke({
        "question": question,
        "result": "",
        "used_tool": False
    })

    return result["result"]


if __name__ == "__main__":

    question = input("Ask the agent: ")

    answer = run_agent(question)

    print("\nAgent:")
    print(answer)