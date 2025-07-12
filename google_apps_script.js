/**
 * Google Apps Script for Tweet Automation
 * Deploy this as a web app to handle GET, POST, and PUT requests
 * for managing tweets in Google Sheets
 * 
 * Sheet structure:
 * Column A: tweet_id (UUID)
 * Column B: tweet (content)
 * Column C: status (pending/done/failed)
 * Column D: created_at (timestamp)
 * Column E: posted_at (timestamp when posted)
 */

// Configuration
const SHEET_NAME = 'Tweets'; // Change this to your sheet name

/**
 * GET request handler - fetch pending tweets
 */
function doGet(e) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
    
    if (!sheet) {
      return ContentService
        .createTextOutput(JSON.stringify({
          status: 'error',
          message: `Sheet '${SHEET_NAME}' not found`
        }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    const data = sheet.getDataRange().getValues();
    const headers = data[0]; // First row contains headers
    
    // Find column indices
    const tweetIdCol = headers.indexOf('tweet_id');
    const tweetCol = headers.indexOf('tweet');
    const statusCol = headers.indexOf('status');
    const createdAtCol = headers.indexOf('created_at');
    
    if (tweetIdCol === -1 || tweetCol === -1 || statusCol === -1) {
      return ContentService
        .createTextOutput(JSON.stringify({
          status: 'error',
          message: 'Required columns not found. Ensure you have: tweet_id, tweet, status'
        }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    // Filter for pending tweets
    const pendingTweets = [];
    
    for (let i = 1; i < data.length; i++) { // Skip header row
      const row = data[i];
      const status = String(row[statusCol]).toLowerCase().trim();
      
      if (status === 'pending') {
        pendingTweets.push({
          tweet_id: row[tweetIdCol],
          tweet: row[tweetCol],
          status: row[statusCol],
          created_at: row[createdAtCol],
          row_number: i + 1 // Store row number for updates
        });
      }
    }
    
    return ContentService
      .createTextOutput(JSON.stringify({
        status: 'success',
        message: `Found ${pendingTweets.length} pending tweets`,
        data: pendingTweets
      }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({
        status: 'error',
        message: `Error fetching tweets: ${error.toString()}`
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * POST request handler - add new tweet
 */
function doPost(e) {
  try {
    const requestBody = JSON.parse(e.postData.contents);
    const { tweet_id, tweet, status = 'pending' } = requestBody;
    
    if (!tweet_id || !tweet) {
      return ContentService
        .createTextOutput(JSON.stringify({
          status: 'error',
          message: 'Missing required fields: tweet_id, tweet'
        }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
    
    if (!sheet) {
      return ContentService
        .createTextOutput(JSON.stringify({
          status: 'error',
          message: `Sheet '${SHEET_NAME}' not found`
        }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    // Add new row
    const timestamp = new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });
    sheet.appendRow([tweet_id, tweet, status, timestamp, '']);
    
    return ContentService
      .createTextOutput(JSON.stringify({
        status: 'success',
        message: 'Tweet added successfully',
        data: { tweet_id, tweet, status, created_at: timestamp }
      }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({
        status: 'error',
        message: `Error adding tweet: ${error.toString()}`
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * PUT request handler - update tweet status
 */
function doPut(e) {
  try {
    const requestBody = JSON.parse(e.postData.contents);
    const { tweet_id, status } = requestBody;
    
    if (!tweet_id || !status) {
      return ContentService
        .createTextOutput(JSON.stringify({
          status: 'error',
          message: 'Missing required fields: tweet_id, status'
        }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
    
    if (!sheet) {
      return ContentService
        .createTextOutput(JSON.stringify({
          status: 'error',
          message: `Sheet '${SHEET_NAME}' not found`
        }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    const data = sheet.getDataRange().getValues();
    const headers = data[0];
    
    // Find column indices
    const tweetIdCol = headers.indexOf('tweet_id');
    const statusCol = headers.indexOf('status');
    const postedAtCol = headers.indexOf('posted_at');
    
    if (tweetIdCol === -1 || statusCol === -1) {
      return ContentService
        .createTextOutput(JSON.stringify({
          status: 'error',
          message: 'Required columns not found'
        }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    // Find the row with matching tweet_id
    let rowFound = false;
    for (let i = 1; i < data.length; i++) {
      if (String(data[i][tweetIdCol]) === String(tweet_id)) {
        // Update status
        sheet.getRange(i + 1, statusCol + 1).setValue(status);
        
        // If status is 'done', update posted_at timestamp
        if (status.toLowerCase() === 'done' && postedAtCol !== -1) {
          const postedTimestamp = new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });
          sheet.getRange(i + 1, postedAtCol + 1).setValue(postedTimestamp);
        }
        
        rowFound = true;
        break;
      }
    }
    
    if (!rowFound) {
      return ContentService
        .createTextOutput(JSON.stringify({
          status: 'error',
          message: `Tweet with ID ${tweet_id} not found`
        }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    return ContentService
      .createTextOutput(JSON.stringify({
        status: 'success',
        message: `Tweet ${tweet_id} status updated to ${status}`,
        data: { tweet_id, status }
      }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({
        status: 'error',
        message: `Error updating tweet: ${error.toString()}`
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Handle unsupported HTTP methods
 */
function doDelete(e) {
  return ContentService
    .createTextOutput(JSON.stringify({
      status: 'error',
      message: 'DELETE method not supported'
    }))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * Test function to create sample data
 */
function createSampleData() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
  
  // Create headers if sheet is empty
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(['tweet_id', 'tweet', 'status', 'created_at', 'posted_at']);
  }
  
  // Add sample tweets
  const sampleTweets = [
    {
      tweet_id: 'sample-uuid-1',
      tweet: 'Hello world! This is a sample tweet for automation testing. #automation #tech',
      status: 'pending'
    },
    {
      tweet_id: 'sample-uuid-2', 
      tweet: 'Another sample tweet to test the cron job functionality. #testing #python',
      status: 'pending'
    },
    {
      tweet_id: 'sample-uuid-3',
      tweet: 'Testing the Google Sheets integration with our tweet automation system! #integration',
      status: 'done'
    }
  ];
  
  const timestamp = new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });
  
  sampleTweets.forEach(tweet => {
    sheet.appendRow([tweet.tweet_id, tweet.tweet, tweet.status, timestamp, '']);
  });
  
  console.log('Sample data created successfully!');
}
