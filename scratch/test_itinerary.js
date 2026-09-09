const https = require('https');

const data = JSON.stringify({
  points: ['Paris', 'Lyon']
});

const options = {
  hostname: 'orbit-backend-122423798285.us-central1.run.app',
  port: 443,
  path: '/api/itinerary',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': data.length
  }
};

const req = https.request(options, (res) => {
  console.log(`Status Code: ${res.statusCode}`);

  let body = '';
  res.on('data', (d) => {
    body += d;
  });

  res.on('end', () => {
    console.log('Response Body:', body);
  });
});

req.on('error', (error) => {
  console.error('Error:', error);
});

req.write(data);
req.end();
