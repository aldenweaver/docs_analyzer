#!/usr/bin/env python3
"""
Quick verification script to test Claude API integration
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("Claude API Configuration Verification")
print("=" * 60)

# Check API key
api_key = os.getenv('ANTHROPIC_API_KEY')
if not api_key:
    print("\n❌ ANTHROPIC_API_KEY is not set!")
    print("\nTo fix:")
    print("1. Edit .env file")
    print("2. Add your API key: ANTHROPIC_API_KEY=sk-ant-api03-xxx")
    print("3. Get your key from: https://console.anthropic.com/")
    sys.exit(1)

print(f"\n✅ ANTHROPIC_API_KEY found: {api_key[:20]}...{api_key[-4:]}")

# Check other settings
enable_ai = os.getenv('ENABLE_AI_ANALYSIS', 'true')
model = os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-5-20250929')
max_tokens = os.getenv('AI_MAX_TOKENS', '2000')

print(f"✅ ENABLE_AI_ANALYSIS: {enable_ai}")
print(f"✅ CLAUDE_MODEL: {model}")
print(f"✅ AI_MAX_TOKENS: {max_tokens}")

# Test API connection
print("\n" + "=" * 60)
print("Testing API Connection")
print("=" * 60)

try:
    import anthropic

    client = anthropic.Anthropic(api_key=api_key)

    # Simple test message
    print("\nSending test request to Claude...")
    message = client.messages.create(
        model=model,
        max_tokens=100,
        messages=[
            {"role": "user", "content": "Say 'API connection successful' if you can read this."}
        ]
    )

    response_text = message.content[0].text
    print(f"\n✅ API Response: {response_text}")

    print("\n" + "=" * 60)
    print("🎉 SUCCESS! Claude API is configured and working!")
    print("=" * 60)
    print("\nYou can now run the analyzer with AI-powered analysis:")
    print("  python doc_analyzer.py /path/to/docs --format all")
    print("\nAI features that will be enabled:")
    print("  • Semantic clarity analysis")
    print("  • Content gap detection")
    print("  • User journey validation")
    print("  • Advanced recommendations")

except ImportError:
    print("\n❌ ERROR: 'anthropic' package not installed")
    print("\nTo fix:")
    print("  pip install anthropic")
    sys.exit(1)

except anthropic.APIError as e:
    print(f"\n❌ API Error: {e}")
    print("\nPossible issues:")
    print("  • Invalid API key")
    print("  • API key expired or revoked")
    print("  • Network connectivity issue")
    print("  • Rate limit exceeded")
    sys.exit(1)

except Exception as e:
    print(f"\n❌ Unexpected error: {e}")
    sys.exit(1)
