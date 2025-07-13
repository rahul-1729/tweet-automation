# Tweet Automation System

Automate tweet scheduling and posting using Python, Google Sheets, and the Twitter/X API. This system fetches tweets from a Google Sheet, posts them to Twitter, and updates their status, all on a schedule.

---

## Features
- **Automated Tweet Posting:** Fetches pending tweets from Google Sheets and posts them to Twitter/X.
- **Status Tracking:** Updates tweet status to "done" or "failed" in the sheet after posting.
- **Scheduling:** Uses APScheduler to run at specific times or intervals.
- **AI Tweet Generation:** (Optional) Generate tweets using LLM agents and submit them to the sheet.
- **Demo/Test Scripts:** Test Google Sheets integration and status updates easily.

---

## Folder Structure
```
tweet-automation/
├── agents/              # AI tweet generation and Google Sheet submission
│   └── agents.py
├── cron/                # Main automation scheduler
│   └── cron.py
├── demo/                # Demo/test scripts
│   └── demo_automation.py
├── tweeter_api/         # Twitter/X API integration
│   └── x_api.py
├── .env                 # Environment variables (not committed)
├── requirements.txt     # Python dependencies
└── Readme.md            # This file
```

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd tweet-automation
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory:
```
API_KEY=your_twitter_api_key
API_KEY_SECRET=your_twitter_api_secret
ACCESS_TOKEN=your_twitter_access_token
ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
GOOGLE_SHEET_LINK=https://script.google.com/macros/s/<YOUR_SCRIPT_ID>/exec
GEMINI_API_KEY=your_gemini_api_key (optional)
```

### 4. Set Up Google Sheet & Apps Script
- Create a Google Sheet with columns: `tweet_id`, `tweet`, `status` .
- Deploy a Google Apps Script as a web app to handle GET/POST requests (see `google_apps_script.js` for sample code).
- Set permissions to "Anyone" and copy the deployment URL to your `.env` as `GOOGLE_SHEET_LINK`.

### Apps Script Code
- Paste the code

```javascript
function doPost(e) {
  try {
    const ss = SpreadsheetApp.openById("<sheet_id>");
    const sheet = ss.getSheetByName("Sheet1");

    var data = JSON.parse(e.postData.contents);
    console.log(data)
    
    // Extract values
    var task = data.task;
    var tweet_id = data.tweet_id;
    var status = data.status

    if (task == "new_tweet")
    {
        var tweet = data.tweet;
        sheet.appendRow([tweet_id,tweet,status]);
        return ContentService.createTextOutput(JSON.stringify({ status: "success", message: "Form submitted" })).setMimeType(ContentService.MimeType.JSON);
    }
    else if (task =="update_tweet")
    {
        if (!tweet_id || !status) {
        throw new Error("Missing 'tweet_id' or 'status'");
      }

      const rows = sheet.getDataRange().getValues();

      // Find the row with the matching tweet_id
      for (let i = 1; i < rows.length; i++) { // start at 1 to skip header
        if (rows[i][0].toString() === tweet_id.toString()) {
          sheet.getRange(i + 1, 3).setValue(status); // column 3 = status
          return ContentService.createTextOutput(
            JSON.stringify({ status: "success", message: "Status updated." })
          )
            .setMimeType(ContentService.MimeType.JSON);
        }
      }

      // If tweet_id not found
      return ContentService.createTextOutput(
        JSON.stringify({ status: "error", message: "tweet_id not found." })
      ).setMimeType(ContentService.MimeType.JSON);
    }
  } catch (err) {
    return ContentService.createTextOutput(
      JSON.stringify({ status: "error", message: err.toString() })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  try {
    const ss = SpreadsheetApp.openById("<sheet_id>");
    const sheet = ss.getSheetByName("Sheet1");

    const data = sheet.getDataRange().getValues(); // includes headers
    const headers = data[0];
    const rows = data.slice(1); // skip header row

    // Filter rows where status is "pending"
    const pendingRows = rows.filter(row => row[2].toLowerCase() === "pending");

    // Convert filtered rows back to objects with header keys
    const result = pendingRows.map(row => {
      let obj = {};
      headers.forEach((header, index) => {
        obj[header] = row[index];
      });
      return obj;
    });

    return ContentService.createTextOutput(
      JSON.stringify({ status: "success", data: result })
    )
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(
      JSON.stringify({ status: "error", message: err.toString() })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}
```

### 5. Configure Twitter/X App
- Create a Twitter/X developer app at https://developer.x.com/en/portal/dashboard
- Set permissions to **Read and Write**.
- Generate and use the API Key, API Secret, Access Token, and Access Token Secret in your `.env` file.

---

## Usage

### **A. Generate Tweets and Add to Sheet (Optional)**
```bash
python agents/agents.py
```
This will use LLM agents to generate tweets and submit them to your Google Sheet with status "pending".

### **B. Run the Cron Scheduler**
#### **1. Scheduled Mode (Recommended)**
Edit the `SCHEDULED_TIME` list in `cron/cron.py` to set your desired posting times (24-hour format):
```python
SCHEDULED_TIME = ['09:00', '13:00', '18:00']
```
Then run:
```bash
python cron/cron.py
```
This will post **one tweet** at each scheduled time.

#### **2. Manual/Immediate Test**
To process and post one tweet immediately:
```bash
python cron/cron.py test
```

### **C. Demo/Test Google Sheets Integration**
```bash
python demo/demo_automation.py
```
This script sends a test POST request to your Apps Script endpoint to update a tweet's status.

---

## How It Works
1. **Tweet Generation:** (Optional) Use `agents.py` to generate tweets and add them to the sheet.
2. **Cron Scheduler:** At each scheduled time, `cron.py` fetches the first pending tweet, posts it to Twitter/X, and updates its status in the sheet.
3. **Status Update:** If posting fails, the status is set to "failed".

---

## Troubleshooting
- **403 Forbidden from Twitter/X:**
  - Ensure your app has **Read and Write** permissions.
  - Regenerate and use new access tokens after changing permissions.
- **Google Sheet Not Updating:**
  - Make sure your Apps Script is deployed as a web app with "Anyone" access.
  - Check the Apps Script logs for errors.
- **No Tweets Being Posted:**
  - Ensure there are rows with status "pending" in your sheet.
  - Check your `.env` and credentials.

---

## Customization
- **Change Posting Times:** Edit `SCHEDULED_TIME` in `cron/cron.py`.
- **Change Sheet Columns:** Update both the Apps Script and Python code to match your sheet structure.
- **Add More AI/LLM Features:** Extend `agents/agents.py` for more advanced tweet generation.

---

## Credits
- Built with Python, Tweepy, APScheduler, Google Apps Script, and OpenAI/Google LLMs.

---

**Happy Automating! **
