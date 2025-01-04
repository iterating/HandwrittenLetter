#!/bin/bash
# Install dependencies
pnpm install --no-frozen-lockfile

# Build the project
pnpm run build

# Ensure dist directory exists
mkdir -p dist

# Move build artifacts if needed
if [ -d "dist" ]; then
  echo "Build successful"
else
  echo "Build failed - no dist directory found"
  exit 1
fi
