#!/usr/bin/env bash
# Script to initialize Git repo and push to GitHub (sonalisadamate)

set -e

echo "🚀 Syncing Git Repository for Multi-Modal Document Intelligence..."

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
git commit -m "refactor: clean line encodings, remove interview files, optimize repo for GitHub view" || echo "No changes to commit."

echo ""
echo "=========================================================================="
echo "🎉 Git Repository Updated & Cleaned!"
echo "=========================================================================="
echo ""
echo "📌 GITHUB PUSH COMMANDS:"
echo ""
echo "Run the following shell commands in your terminal to update GitHub:"
echo "   cd /Users/indrajeetrajaramsadamate/.gemini/antigravity/scratch/multimodal_doc_intelligence"
echo "   git push -u origin main --force"
echo ""
echo "=========================================================================="
