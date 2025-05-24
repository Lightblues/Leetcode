#!/bin/bash

# Commit and push to GitHub
# Usage: ./auto_commit.sh [commit message]

# Change directory to project root (one level up from script location)
cd "$(git rev-parse --show-toplevel)"

# Get current time as default commit message
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
COMMIT_MESSAGE="${1:-Auto commit: $TIMESTAMP}"

# Check for changes
if [[ -z $(git status --porcelain) ]]; then
    echo "No changes to commit."
    exit 0
fi

# Pull latest changes from remote repository
echo "Pulling latest changes from remote repository..."
git pull origin main --rebase

# Add changes
git add .

# Commit changes
git commit -m "$COMMIT_MESSAGE"

# Push to remote repository
git push origin main

echo "Successfully committed and pushed changes to GitHub."
echo "Commit message: $COMMIT_MESSAGE"
