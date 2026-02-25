@echo off
REM Silver Tier Setup Script for Windows

echo ==================================
echo Silver Tier - Complete Setup
echo ==================================

REM Step 1: Install Python dependencies
echo.
echo [1/5] Installing Python dependencies...
cd silver-tier\watchers
pip install google-api-python-client google-auth-oauthlib playwright
echo OK - Python dependencies installed

REM Step 2: Install Playwright browsers
echo.
echo [2/5] Installing Playwright browsers...
playwright install chromium
echo OK - Playwright installed

REM Step 3: Install Email MCP
echo.
echo [3/5] Installing Email MCP server...
cd ..\mcp-servers\email-mcp
call npm install
echo OK - Email MCP installed

REM Step 4: Setup instructions
echo.
echo [4/5] Manual Setup Required:
echo.
echo GMAIL WATCHER:
echo   1. Go to: https://console.cloud.google.com/apis/credentials
echo   2. Create OAuth 2.0 credentials
echo   3. Save to: C:\Users\YourName\.gmail_credentials.json
echo.
echo WHATSAPP WATCHER:
echo   1. Run: python whatsapp_watcher.py
echo   2. Scan QR code in browser
echo.
echo LINKEDIN POSTER:
echo   1. Run: python linkedin_poster.py --setup
echo   2. Log in to LinkedIn
echo.

REM Step 5: Done
echo [5/5] Setup complete!
echo.
echo Run watchers:
echo   cd silver-tier\watchers
echo   python filesystem_watcher.py  -- File monitoring
echo   python gmail_watcher.py       -- Gmail monitoring
echo   python whatsapp_watcher.py   -- WhatsApp monitoring
echo.
echo Run MCP server:
echo   cd silver-tier\mcp-servers\email-mcp
echo   node index.js

pause
