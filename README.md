# 🤖 LangGraph Agent

A simple Agentic AI application built using **LangGraph, LangChain, Google Gemini, and Streamlit**.

The agent can understand a user's question, decide whether a calculator tool is needed, use the tool when required, and return the final answer.

## 🚀 Live Demo

(https://langgraph-agent-2atcr4flelzaildm3bt6te.streamlit.app/)

## 📌 Project Overview

This project demonstrates the basic concept of **Agentic AI** using LangGraph.

The agent handles two types of requests:

- General questions → answered using Google Gemini
- Mathematical questions → handled using a custom Calculator Tool

## 🧠 How It Works

```text
User Question
      ↓
   LangGraph
      ↓
   Decision
   ↙     ↘
Math     Normal Question
 ↓            ↓
Calculator   Gemini
   ↘         ↙
      Final Answer
           ↓
          User
