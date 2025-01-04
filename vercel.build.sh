#!/bin/bash

# Install frontend dependencies and build
cd client
pnpm install
pnpm run build

# Move back to root
cd ..
