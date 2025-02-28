# Multi-Agent-Application--Stock-Report--Vaisakh-krishna-U-B--harikonny97-gmail.com

Overview

This Multi-Agent Stock Analysis System automates stock evaluation using AI-driven agents that fetch financial data, analyze trends, and generate structured investment reports. It utilizes Yahoo Finance (yfinance) for stock data retrieval, DeepSeek LLM for analysis, and LangGraph for multi-agent coordination. The system produces a professional investment report, including:

Summary

Key Observations

Risk Assessment

Recommendation (Buy/Hold/Sell)


Features

Automated Data Retrieval: Fetches stock data using yfinance.

AI-Powered Analysis: Uses DeepSeek LLM to analyze trends and key insights.

Structured Investment Report: Generates clear and concise reports for informed decision-making.

Multi-Agent Coordination: Utilizes LangGraph to efficiently manage AI agents.


Installation

To set up and run the project, follow these steps:

1. Clone the Repository

git clone https://github.com/pineaplonpizza/Multi-Agent-Application--Stock-Report--Vaisakh-krishna-U-B--harikonny97-gmail.com.git

cd multi-agent-stock-analysis


2. Create and Activate a Virtual Environment

python -m venv venv  # Create virtual environment

source venv/bin/activate  # For macOS/Linux

venv\Scripts\activate  # For Windows


3. Install Dependencies

pip install -r requirements.txt

4. Set Up Environment Variables

Create a .env file in the project directory and add your Groq API Key:

GROQ_API_KEY=your_api_key_here

5. Run the Program

python stock_analysis.py

Usage

Once the program starts, enter the stock ticker symbol (e.g., AAPL for Apple) when prompted. The system will:

Fetch stock data from Yahoo Finance.

Analyze price trends, volume, and support/resistance levels.

Generate a structured investment report.

Display the final report in the terminal.
