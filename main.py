import yfinance as yf
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from groq import Groq
from typing import TypedDict, Annotated
import os
from dotenv import load_dotenv
import re

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

class AgentState(TypedDict):
    symbol: str
    data: dict
    analysis: Annotated[str, add_messages]
    report: Annotated[str, add_messages]

# Define our agents
class FinancialDataFetcher:
    def run(self, state: AgentState) -> dict:
        """Fetch stock data using yfinance"""
        print("Fetching data for:", state["symbol"])
        ticker = yf.Ticker(state["symbol"])
        hist = ticker.history(period="1mo")
        return {
            "data": {
                "current_price": hist['Close'].iloc[-1],
                "30d_high": hist['Close'].max(),
                "30d_low": hist['Close'].min(),
                "volume": hist['Volume'].mean()
            }
        }

class AnalysisAgent:
    def run(self, state: AgentState) -> dict:
        """Analyze financial data using LLM"""
        print("Analyzing data...")
        prompt = f"""Analyze this stock data:
        {state["data"]}
        
        Provide a brief technical analysis focusing on:
        - Current price position
        - Recent performance
        - Volume trends
        - Potential support/resistance levels"""

        response = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return {"analysis": response.choices[0].message.content}

class ReportGenerator:
    def run(self, state: AgentState) -> dict:
        """Generate final report using LLM"""
        print("Generating report...")
        prompt = f"""Create an investment report for {state["symbol"]} based on this analysis:
        {state["analysis"]}
        
        Structure the report with:
        - Summary
        - Key Observations
        - Risk Assessment
        - Recommendation (Buy/Hold/Sell)
        
        Keep sure that there is a clear segmentation of each section and its easy to read."""

        response = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return {"report": response.choices[0].message.content}

# Set up LangGraph workflow
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("data_fetcher", FinancialDataFetcher().run)
workflow.add_node("analyst", AnalysisAgent().run)
workflow.add_node("reporter", ReportGenerator().run)

# Define edges
workflow.set_entry_point("data_fetcher")
workflow.add_edge("data_fetcher", "analyst")
workflow.add_edge("analyst", "reporter")
workflow.add_edge("reporter", END)

# Compile the workflow
chain = workflow.compile()

def analyze_stock(symbol: str):
    # Run the system with initial state
    initial_state = AgentState(
        symbol=symbol,
        data={},
        analysis="",
        report=""
    )
    results = chain.invoke(initial_state)

    # Display final report
    print("\nFinal Report:")
    print("="*100)
    print(results["report"][2])

if __name__ == "__main__":
    print("Welcome to Stock Analysis System")
    print("Please enter the stock ticker symbol you want to analyze:")
    symbol = input()
    analyze_stock(symbol)