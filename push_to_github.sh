#!/usr/bin/env bash
# Script to initialize Git repo and push to GitHub (sonalisadamate)

set -e

echo "🚀 Setting up Git Repository for Multi-Modal Document Intelligence..."

# Ensure we are in project directory
cd "$(dirname "$0")"

export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null

if [ ! -d ".git" ]; then
    git init
    echo "✅ Git repository initialized."
fi

git config user.name "sonalisadamate"
git config user.email "sonalisadamate@users.noreply.github.com"
git branch -M main

git add .
git commit -m "feat: complete multi-modal document intelligence platform with RAG, guardrails, RAGAS, and Streamlit UI" || echo "No changes to commit."

echo ""
echo "=========================================================================="
echo "🎉 Local Git Repository Committed to 'main'!"
echo "=========================================================================="
echo ""
echo "📌 GITHUB PUSH INSTRUCTIONS:"
echo ""
echo "1️⃣ Create a new repo named 'Multi-Modal-Document-Intelligence' on GitHub:"
echo "   https://github.com/new"
echo "   (Do not select 'Initialize with README' since README is already committed locally)"
echo ""
echo "2️⃣ Run the following shell commands to push your project:"
echo "   cd /Users/indrajeetrajaramsadamate/.gemini/antigravity/scratch/multimodal_doc_intelligence"
echo "   git remote add origin https://github.com/sonalisadamate/Multi-Modal-Document-Intelligence.git"
echo "   git push -u origin main"
echo ""
echo "3️⃣ UPDATE YOUR GITHUB PROFILE README (https://github.com/sonalisadamate/sonalisadamate):"
echo "   In your Profile README, under the 'Projects' section, add this entry ABOVE 'Agentic AI Framework':"
echo ""
echo "   ### 🧠 [Multi-Modal Document Intelligence](https://github.com/sonalisadamate/Multi-Modal-Document-Intelligence)"
echo "   - Enterprise multi-modal document intelligence platform that extracts, cites, summarizes, and answers Q&A on PDFs, scans, tables, and images."
echo "   - **Tech Stack**: LangChain, Vision LLMs (GPT-4o/Gemini), Multimodal RAG, ChromaDB & Pinecone, PII & Prompt-Injection Guardrails, LangSmith, RAGAS Eval, Streamlit."
echo "=========================================================================="
