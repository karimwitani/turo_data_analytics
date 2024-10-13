// background.js

const sessions = {};

// Start recording network traffic
async function startRecording(tabId) {
    tabId = parseInt(tabId, 10); // Ensure tabId is an integer
    if (sessions[tabId]) {
        console.log('Recording already in progress for this tab.');
        return;
    }

    try {
        await chrome.debugger.attach({ tabId }, '1.3');
        sessions[tabId] = { events: [] };

        chrome.debugger.onEvent.addListener(onEvent);
        chrome.debugger.onDetach.addListener(onDetach);

        await chrome.debugger.sendCommand({ tabId }, 'Network.enable');
        console.log('Started recording on tab', tabId);
    } catch (error) {
        console.error('Failed to attach debugger:', error);
    }
}

// Stop recording and generate HAR file
async function stopRecording(tabId) {
    tabId = parseInt(tabId, 10); // Ensure tabId is an integer
    if (!sessions[tabId]) {
        console.log('No recording session found for this tab.');
        return;
    }

    try {
        // Get the recorded events
        const { events } = sessions[tabId];
        delete sessions[tabId];

        // Remove event listeners to stop capturing new events
        chrome.debugger.onEvent.removeListener(onEvent);
        chrome.debugger.onDetach.removeListener(onDetach);

        // Process the events and create the HAR log
        const harLog = await createHarLog(events, tabId);

        // Download the HAR file
        downloadHarFile(harLog);

        // Now that we're done processing, disable network tracking and detach the debugger
        await chrome.debugger.sendCommand({ tabId }, 'Network.disable');
        await chrome.debugger.detach({ tabId });

        console.log('Stopped recording on tab', tabId);
    } catch (error) {
        console.error('Failed to stop recording:', error);
    }
}


// Handle network events
function onEvent(debuggeeId, message, params) {
    const tabId = debuggeeId.tabId;
    if (sessions[tabId]) {
        if (message === 'Network.requestWillBeSent' || message === 'Network.responseReceived') {
            sessions[tabId].events.push({ message, params });
        }
    }
}

// Handle debugger detachment
function onDetach(debuggeeId, reason) {
    const tabId = debuggeeId.tabId;
    if (sessions[tabId]) {
        delete sessions[tabId];
        console.log('Debugger detached from tab', tabId, 'due to', reason);
    }
}

// Create HAR log from events
async function createHarLog(events, tabId) {
    const harLog = {
        data_type: "Turo Search Page Results",
        timestamp: new Date(request.wallTime * 1000).toISOString(),
        entries: []
    };

    const requestMap = {};

    for (const event of events) {
        const requestId = event.params.requestId;

        if (event.message === 'Network.requestWillBeSent') {
            const url = event.params.request.url;

            // Filter requests to include only specific URLs
            if (
                // url.includes('turo.com/api/bulk-quotes/v2') ||
                // url.includes('turo.com/api/v2/search/')
                url == "https://turo.com/api/v2/search"
            ) {
                if (!requestMap[requestId]) requestMap[requestId] = {};
                requestMap[requestId].request = event.params;
                console.log(`Captured request for ${requestId}: ${url}`);
            } else {
                // Skip non-matching requests
                continue;
            }
        } else if (event.message === 'Network.responseReceived') {
            if (requestMap[requestId]) {
                requestMap[requestId].response = event.params;
                console.log(`Captured response for ${requestId}`);
            }
        }
    }

    for (const requestId in requestMap) {
        const data = requestMap[requestId];

        // Ensure both request and response are present
        if (data.request && data.response) {
            const entry = await buildHarEntry(data, requestId, tabId);
            if (entry) {
                harLog.entries.push(entry);
            }
        } else {
            console.log(`Incomplete data for requestId ${requestId}, skipping.`);
        }
    }

    return harLog;
}


// Build individual HAR entry
async function buildHarEntry(data, requestId, tabId) {
    tabId = parseInt(tabId, 10); // Ensure tabId is an integer
    const { request, response } = data;
    if (!request || !response) return null;

    console.log(response.response.url);
    console.log(response);
    console.log(request);

    // Get response body
    let body = '';
    let encoding = '';
    let parsedBody = null; // Variable to hold the parsed JSON
    
    try {
        const result = await chrome.debugger.sendCommand(
            { tabId },
            'Network.getResponseBody',
            { requestId }
        );
        body = result.body || '';
        if (result.base64Encoded) {
            encoding = 'base64';
            // Decode the Base64 string
            body = atob(body);
        }

        // Parse the JSON string
        parsedBody = JSON.parse(body);
        console.log('Parsed response body:', parsedBody);

    } catch (error) {
        console.warn('Failed to get response body for', requestId, error);
    }

    // Log the body for debugging
    console.log(`Response body for requestId ${requestId}:`, body);

    return {
        request_method: request.request.method,
        request_url: request.request.url,
        response_status:response.response.status, 
        response_status_text: response.response.statusText,
        response_content : parsedBody
    };
}


// Helper to format headers
function formatHeaders(headers) {
    return Object.entries(headers || {}).map(([name, value]) => ({ name, value }));
}

// Helper to parse query string
function formatQueryString(url) {
    const query = new URL(url).searchParams;
    const queryString = [];
    for (const [name, value] of query.entries()) {
        queryString.push({ name, value });
    }
    return queryString;
}

// Download HAR file
function downloadHarFile(harLog) {
    const harData = JSON.stringify(harLog, null, 2);
    const blob = new Blob([harData], { type: 'application/json' });

    const reader = new FileReader();
    reader.onloadend = function () {
        const dataURL = reader.result;

        chrome.downloads.download({
            url: dataURL,
            filename: 'network_requests.har',
            saveAs: true
        }, (downloadId) => {
            if (chrome.runtime.lastError) {
                console.error('Error downloading HAR file:', chrome.runtime.lastError);
            } else {
                console.log('HAR file download initiated. Download ID:', downloadId);
            }
        });
    };
    reader.readAsDataURL(blob);
}

// Listen for messages from popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs.length === 0) return;

        let tabId = tabs[0].id;
        tabId = parseInt(tabId, 10); // Ensure tabId is an integer

        if (message.type === 'start') {
            startRecording(tabId);
        } else if (message.type === 'stop') {
            stopRecording(tabId);
        }
    });
});
