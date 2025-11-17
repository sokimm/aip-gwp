#!/bin/bash
# Setup python alias for this project

echo "Setting up Python alias for this session..."
echo "You can run 'python' and it will use python3.11"
echo ""

# Create alias for current session
alias python='python3.11'
alias pip='python3.11 -m pip'

echo "✓ Alias created:"
echo "  python -> python3.11"
echo "  pip -> python3.11 -m pip"
echo ""
echo "To make this permanent, add these lines to your ~/.zshrc or ~/.bashrc:"
echo "  alias python='python3.11'"
echo "  alias pip='python3.11 -m pip'"
