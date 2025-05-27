#!/bin/bash

# Commit and push to GitHub
# Usage: ./auto_commit.sh [commit message]

# Change directory to project root (current dir, then git root)
cd $(dirname "$0")
cd "$(git rev-parse --show-toplevel)"
echo "Current directory: $(pwd)"

# Get current time as default commit message
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
COMMIT_MESSAGE="${1:-Auto commit: $TIMESTAMP}"

# Check for changes
if [[ -z $(git status --porcelain) ]]; then
    echo "No changes to commit."
else
    # Add changes
    git add .
    # Commit changes
    git commit -m "$COMMIT_MESSAGE"
    echo "Commit message: $COMMIT_MESSAGE"
fi

# Pull latest changes from remote repository
echo "Pulling latest changes from remote repository..."
git pull origin main --rebase

# Push to remote repository
git push origin main

echo "Successfully committed and pushed changes to GitHub."
