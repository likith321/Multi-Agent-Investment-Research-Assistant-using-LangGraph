"""
Demo-only graph for Review 1.

This wires together ONLY the two nodes that run with zero external
API keys (no Groq LLM calls, no embeddings/vectorstore setup):

    Data Gatherer  ->  Fundamental Analyst

Everything imported here (ResearchState, the two agent functions,
the audit store) is the SAME code used by the full pipeline in
orchestration/graph.py -- nothing is faked or reimplemented for the
demo. The remaining agents (retrieval, sentiment, risk, report
writer, critic) are already written in agents/, they are just not
wired into this smaller graph so the live demo doesn't depend on an
API key or internet-dependent LLM call.
"""

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from state.research_state import ResearchState
from agents.data_gatherer import data_gatherer
from agents.fundamental_analyst import fundamental_analyst

demo_graph = StateGraph(ResearchState)

demo_graph.add_node("data_gatherer", data_gatherer)
demo_graph.add_node("fundamental_analyst", fundamental_analyst)

demo_graph.set_entry_point("data_gatherer")

demo_graph.add_edge("data_gatherer", "fundamental_analyst")
demo_graph.add_edge("fundamental_analyst", END)

checkpointer = MemorySaver()

demo_app = demo_graph.compile(checkpointer=checkpointer)
