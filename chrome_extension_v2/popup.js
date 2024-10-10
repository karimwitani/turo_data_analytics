document.getElementById('start').addEventListener('click', () => {
    chrome.runtime.sendMessage({ type: 'start' });
  });
  
  document.getElementById('stop').addEventListener('click', () => {
    chrome.runtime.sendMessage({ type: 'stop' });
  });
  