#!/usr/bin/env bash
# Script to initialize Git repo and provide push commands for GitHub

set -e

echo "🚀 Initializing Git Repository for Multi-Modal Document Intelligence..."

# Ensure we are in project directory
cd "$(dirname "$0")"

# Initialize Git
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git repository initialized."
fi

# Configure local git user credentials for sonalisadamate
git config user.name "sonalisadamate"
git config user.email "sonalisadamate@users.noreply.github.com"

# Stage all project files
git add .

# Initial commit
git commit -m "feat: complete multi-modal document intelligence platform with RAG, guardrails, RAGAS, and Streamlit UI" || echo "No new changes to commit."

# Set main branch
git branch -M main

echo ""
echo "=========================================================================="
echo "🎉 Local Git Repository is Ready & Committed!"
echo "=========================================================================="
echo ""
echo "📌 NEXT STEPS TO PUBLISH TO GITHUB:"
echo ""
echo "1️⃣ Go to GitHub: https://github.com/new"
echo "   • Repository Name: Multi-Modal-Document-Intelligence"
echo "   • Description: Multi-Modal Document Intelligence with Vision LLMs, OCR, Multimodal RAG, LangChain, ChromaDB, Guardrails, and Streamlit UI"
echo "   • Public/Private: Public"
echo "   • Do NOT initialize with README (already created locally)"
echo ""
echo "2️⃣ Run the following commands in your terminal to push:"
echo "   cd /Users/indrajeetrajaramsadamate/.gemini/antigravity/scratch/multimodal_doc_intelligence"
echo "   git remote add origin https://github.com/sonalisadamate/Multi-Modal-Document-Intelligence.git"
echo "   git push -u origin main"
echo ""
echo "3️⃣ UPDATE YOUR GITHUB PROFILE README (https://github.com/sonalisadamate/sonalisadamate):"
echo "   Add this section above your 'Agentic AI Framework' project:"
echo ""
echo "   ### 🧠 [Multi-Modal Document Intelligence](https://github.com/sonalisadamate/Multi-Modal-Document-Intelligence)"
echo "   - Enterprise multi-modal document intelligence platform extracting, citing, summarizing, and answering Q&A on PDFs, scans, tables, and images."
echo "   - **Tech Stack**: LangChain, Vision LLMs (GPT-4o/Gemini), Multimodal RAG, ChromaDB & Pinecone, PII & Prompt-Injection Guardrails, LangSmith, RAGAS Eval."
echo "=========================================================================="
