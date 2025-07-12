# Tweet Automation Setup Guide

## 🚀 Complete Tweet Automation System

This system automatically fetches pending tweets from a Google Sheet, posts them to Twitter, and updates their status to "done" using a cron job scheduler.

## 📋 Prerequisites

1. **Python 3.8+**
2. **Twitter Developer Account** with API keys
3. **Google Account** for Google Sheets
4. **Google Apps Script** for API endpoints

## 🛠️ Installation

### 1. Install Dependencies

```powershell
cd "c:\Users\b-rahulkumar\Documents\fun_project_for_automation\Tweeter\tweet-automation"
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file in the root directory:

```env
# Twitter API Credentials
API_KEY=your_twitter_api_key
API_KEY_SECRET=your_twitter_api_secret
ACCESS_TOKEN=your_twitter_access_token
ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

# Google Sheets API URL (from Google Apps Script deployment)
GOOGLE_SHEET_LINK=https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec

# Gemini API for tweet generation (optional)
GEMINI_API_KEY=your_gemini_api_key
```

### 3. Google Sheets Setup

#### Step 3.1: Create Google Sheet
1. Create a new Google Sheet
2. Add these column headers in row 1:
   - A1: `tweet_id`
   - B1: `tweet`
   - C1: `status`
   - D1: `created_at`
   - E1: `posted_at`

#### Step 3.2: Deploy Google Apps Script
1. Open Google Apps Script (script.google.com)
2. Create a new project
3. Copy the code from `google_apps_script.js`
4. Replace `SHEET_NAME` with your sheet name
5. Deploy as web app:
   - Execute as: Me
   - Who has access: Anyone
6. Copy the deployment URL to your `.env` file

## 🎮 Usage

### Demo Mode (Recommended for Testing)

```powershell
# Interactive demo with mock data
python demo/demo_automation.py

# Cron scheduler in demo mode (simulates posting)
python cron/cron.py --mode demo
```

### Production Mode

```powershell
# Run every minute (real Twitter posting)
python cron/cron.py --mode production

# Run at specific times daily (9 AM, 1 PM, 6 PM IST)
python cron/cron.py --mode specific-time
```

### Generate and Add Tweets

```powershell
# Generate tweets using AI agents and add to Google Sheets
python agents/agents.py
```

## 📊 System Workflow

```
1. 📥 Fetch pending tweets from Google Sheets (GET request)
2. 🐦 Post each tweet to Twitter (Twitter API)
3. ✅ Update tweet status to "done" (PUT request)
4. ⏰ Repeat based on cron schedule
```

## 🔧 Configuration Options

### Cron Scheduler Modes

1. **Production Mode**: Posts to real Twitter, runs every minute
2. **Demo Mode**: Simulates posting, safe for testing
3. **Specific Time Mode**: Runs at configured times (9 AM, 1 PM, 6 PM IST)

### Customizing Schedule Times

Edit the `start_specific_time_cron()` function in `cron/cron.py`:

```python
# Modify these times (24-hour format)
times_to_run = ['09:00', '13:00', '18:00']
```

## 📁 File Structure

```
tweet-automation/
├── agents/
│   ├── agents.py          # AI tweet generation
│   ├── constants.py       # Configuration constants
│   └── prompt.py          # AI prompts
├── cron/
│   └── cron.py           # Main cron scheduler
├── demo/
│   └── demo_automation.py # Interactive demo
├── tweeter_api/
│   └── x_api.py          # Twitter API functions
├── google_apps_script.js  # Google Apps Script code
├── requirements.txt       # Python dependencies
└── .env                  # Environment variables
```

## 🛡️ Safety Features

- **Demo Mode**: Test without real API calls
- **Error Handling**: Failed tweets marked as "failed"
- **Logging**: Detailed status messages
- **Rate Limiting**: Respects Twitter API limits
- **Character Validation**: Checks tweet length

## 📝 Google Sheets API Endpoints

The Google Apps Script handles:

- **GET**: Fetch pending tweets
- **POST**: Add new tweets
- **PUT**: Update tweet status

## 🔍 Troubleshooting

### Common Issues

1. **"Sheet not found"**: Check `SHEET_NAME` in Google Apps Script
2. **API authentication errors**: Verify Twitter API keys
3. **Google Apps Script errors**: Check deployment permissions
4. **Time zone issues**: System uses IST (Asia/Kolkata)

### Debug Mode

Run with verbose logging:

```powershell
python cron/cron.py --mode demo  # See detailed output
```

## 🎯 Testing Workflow

1. **Start with Demo Mode**:
   ```powershell
   python demo/demo_automation.py
   ```

2. **Test Cron in Demo Mode**:
   ```powershell
   python cron/cron.py --mode demo
   ```

3. **Add Real Tweets to Sheet**:
   ```powershell
   python agents/agents.py
   ```

4. **Run Production Mode**:
   ```powershell
   python cron/cron.py --mode production
   ```

## 📈 Monitoring

The system provides real-time feedback:
- ✅ Successful operations
- ❌ Failed operations  
- 📊 Statistics summary
- ⏰ Timestamp logs

## 🔧 Customization

### Adding Custom Tweet Sources

Modify `agents/agents.py` to integrate with:
- RSS feeds
- News APIs
- Custom content generators

### Custom Scheduling

Modify `cron/cron.py` for:
- Different time intervals
- Complex scheduling patterns
- Multiple daily runs

## 🚨 Important Notes

- **Always test in demo mode first**
- **Monitor Twitter API rate limits**
- **Keep API keys secure**
- **Backup your Google Sheet**
- **Check tweet content before posting**

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review log messages
3. Test individual components
4. Verify API credentials

---
*Happy Tweeting! 🐦✨*
