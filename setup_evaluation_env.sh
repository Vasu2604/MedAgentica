#!/bin/bash

# Setup script for RAG & LLM Evaluation Environment
# This script helps configure environment variables and install dependencies

echo "🔧 Setting up RAG & LLM Evaluation Environment..."
echo ""

# Check if .env file exists
if [ -f .env ]; then
    echo "✅ Found existing .env file"
    echo "⚠️  Will append to existing .env (won't overwrite existing values)"
else
    echo "📝 Creating new .env file"
    touch .env
fi

echo ""
echo "Please provide your API keys and configuration:"
echo ""

# Prompt for API keys
read -p "Enter your PINECONE_API_KEY (press Enter to skip if already set): " pinecone_key
read -p "Enter your PINECONE_INDEX_NAME [default: medagentica]: " pinecone_index
read -p "Enter your OPENROUTER_API_KEY (press Enter to skip if already set): " openrouter_key
read -p "Enter your OPENROUTER_MODEL [default: deepseek/deepseek-chat-v3.1:free]: " openrouter_model

# Set defaults
pinecone_index=${pinecone_index:-medagentica}
openrouter_model=${openrouter_model:-deepseek/deepseek-chat-v3.1:free}

echo ""
echo "💾 Saving to .env file..."

# Function to update or append to .env
update_env() {
    key=$1
    value=$2
    
    if [ ! -z "$value" ]; then
        # Check if key exists in .env
        if grep -q "^${key}=" .env 2>/dev/null; then
            # Update existing
            if [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS
                sed -i '' "s|^${key}=.*|${key}=${value}|" .env
            else
                # Linux
                sed -i "s|^${key}=.*|${key}=${value}|" .env
            fi
            echo "   ✅ Updated ${key}"
        else
            # Append new
            echo "${key}=${value}" >> .env
            echo "   ✅ Added ${key}"
        fi
    else
        echo "   ⏭️  Skipped ${key}"
    fi
}

# Update .env file
update_env "PINECONE_API_KEY" "$pinecone_key"
update_env "PINECONE_INDEX_NAME" "$pinecone_index"
update_env "OPENROUTER_API_KEY" "$openrouter_key"
update_env "OPENROUTER_MODEL" "$openrouter_model"

echo ""
echo "📦 Installing missing Python packages..."
pip install rouge-score pdfplumber -q

echo ""
echo "🔄 Loading environment variables..."
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "   ✅ Environment variables loaded"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Load environment variables in your current shell:"
echo "   source .env"
echo "   OR"
echo "   export \$(cat .env | grep -v '^#' | xargs)"
echo ""
echo "2. Verify setup:"
echo "   python check_evaluation_setup.py"
echo ""
echo "3. If Pinecone index is empty, ingest data:"
echo "   python demo_ingest_pinecone.py"
echo ""
echo "4. Run your first evaluation:"
echo "   python quick_evaluate.py"
echo ""

