from typing import TypedDict
from typing_extensions import Annotated
from langgraph.graph.message import add_messages
from agents.interface import interface_llm, router_decision
from agents.factual import factual_llm
from agents.conversational import conversational_llm

class State(TypedDict):
    messages : Annotated[list, add_messages]

from langgraph.graph import StateGraph, START, END    

def create_graph():
    graph_builder = StateGraph(State)


#add nodes
    graph_builder.add_node("interface_node", interface_llm)
    graph_builder.add_node("factual_node", factual_llm)
    graph_builder.add_node("conversational_node", conversational_llm)



#add edges
    graph_builder.add_edge(START, "interface_node")
    graph_builder.add_conditional_edges(
       "interface_node",
          router_decision,
        {
            "factual_node": "factual_node",
            "conversational_node": "conversational_node",
        
       }
   )
    graph_builder.add_edge("factual_node", END)
    graph_builder.add_edge("conversational_node", END)


    return  graph_builder.compile()

graph = create_graph()
