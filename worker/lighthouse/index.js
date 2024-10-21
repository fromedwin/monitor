import fetch from 'node-fetch';
import amqp from 'amqplib';

// Load lighthouse and chrome-launcher to setup lighthouse locally
import lighthouse from 'lighthouse';
import chromeLauncher from 'chrome-launcher';

let UUID = process.env.UUID;
let SERVER_URL = process.env.SERVER_URL;
const SECRET_KEY = process.env.SECRET_KEY;
const CELERY_BROKER_URL = process.env.CELERY_BROKER_URL;
const USER_AGENT = 'fromedwin bot lighthouse worker';

// Request performance object entrypoint
let url = `${SERVER_URL}/api/request/${UUID}/performance`

if (process.env.DISABLE_PERFORMANCE == 1) {
	console.log('❌  DISABLE_PERFORMANCE == 1, disabling lighthouse report');
	process.exit(1);
}

// Constant copied from https://github.com/GoogleChrome/lighthouse/blob/main/core/config/constants.js
const DESKTOP_EMULATION_METRICS = {
  mobile: false,
  width: 1350,
  height: 940,
  deviceScaleFactor: 1,
  disabled: false,
};

const MOTOGPOWER_EMULATION_METRICS = {
  mobile: true,
  width: 412,
  height: 823,
  // This value has some interesting ramifications for image-size-responsive, see:
  // https://github.com/GoogleChrome/lighthouse/issues/10741#issuecomment-626903508
  deviceScaleFactor: 1.75,
  disabled: false,
};

const screenEmulationMetrics = {
  mobile: MOTOGPOWER_EMULATION_METRICS,
  desktop: DESKTOP_EMULATION_METRICS,
};

const MOTOG4_USERAGENT = 'Mozilla/5.0 (Linux; Android 11; moto g power (2022)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36 fromedwin'; // eslint-disable-line max-len
const DESKTOP_USERAGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 fromedwin'; // eslint-disable-line max-len

/**
 * Start infinite to start generating lighthouse reports
 **/
const QUEUE_NAME = 'fromedwin_lighthouse_queue';  // The same queue specified in Python

(async () => {
	try {
	  const connection = await amqp.connect(CELERY_BROKER_URL);
	  const channel = await connection.createChannel();

	  // Set prefetch to 1 to limit to one message at a time
	  channel.prefetch(1);

	  // Ensure the queue exists
	  await channel.assertQueue(QUEUE_NAME, { durable: true });
  
	  console.log(`Listening for tasks in queue: ${QUEUE_NAME}`);
  
	  // Consume messages from the specified queue
	  channel.consume(QUEUE_NAME, async (msg) => {
		if (msg !== null) {
		  const message = JSON.parse(msg.content.toString());
  
		  console.log('received task', msg.properties?.headers?.task);
		  if (msg.properties?.headers?.task === 'fetch_lighthouse_report') {
			console.log('received message', message);
			const args = message[0];
			const kwargs = message[1];
			console.log(`Received task: ${msg.properties?.headers?.task}`);
			console.log(`Args: ${args}`);
			console.log(`Kwargs: ${kwargs}`);
			// Process the task here

			console.log(`Running test on ${kwargs.url}`);

			// Start Chrome process
			const chrome = await chromeLauncher.launch({
				ignoreDefaultFlags: true,
				chromeFlags: [
						'--headless',
						'--no-sandbox',
						'--disable-dev-shm-usage',
						'--allow-pre-commit-input',
						'--in-process-gpu',
					]
				}); //  '--disable-gpu', '--disable-setuid-sandbox'

			// Running Lighthouse by custom options
			const options = {
				logLevel: 'info', 
				output: 'json', 
				port: chrome.port,
				formFactor: 'desktop', // 'desktop' or 'mobile'
				screenEmulation: screenEmulationMetrics.desktop,
				emulatedUserAgent: DESKTOP_USERAGENT, //MOTOG4_USERAGENT,
				skipAudits: [
					// Skip the h2 audit so it doesn't lie to us. See https://github.com/GoogleChrome/lighthouse/issues/6539
					'uses-http2',
					// There are always bf-cache failures when testing in headless. Reenable when headless can give us realistic bf-cache insights.
					'bf-cache',
				],
			};
			const runnerResult = await lighthouse(kwargs.url, options);

			console.log(`Saving report for ${kwargs.url}`);
			// Send report to server
			const reportResponse = await fetch(`${SERVER_URL}/api/report/${SECRET_KEY}/performance/${kwargs.id}`, {
				method: 'POST',
				headers: {
					'User-Agent': USER_AGENT,
					'Content-Type': 'application/json'
				},
				body: runnerResult.report
			}).then((returnedResponse) => {
				console.log("Report has been forwarded http status", returnedResponse.status)
			}).catch((error) => {
				console.error(error)
			});
			console.log(`Test is done for ${kwargs.url}`);

			// Kill chrome process
			await chrome.kill();

			// Acknowledge the message
			channel.ack(msg);
		  } else {
			// Ignore or reject messages that don't match
			channel.nack(msg);
		  }
		}
	  });
	} catch (err) {
	  console.error('Error connecting to RabbitMQ:', err);
	}
  })();


// while(true) {
// 	// Fetch url from docker
// 	try {
// 		// Fetch next performance object to evaluate
// 		const response = await fetch(url, {
// 			headers: {
// 				'User-Agent': USER_AGENT,
// 			}
// 		});
// 		const data = await response.json();

// 		if (data && data.performance && data.performance.url) {

// 			console.log(`Running test on ${data.performance.url}`);

// 			// Start Chrome process
// 			const chrome = await chromeLauncher.launch({
// 				ignoreDefaultFlags: true,
// 				chromeFlags: [
// 						'--headless',
// 						'--no-sandbox',
// 						'--disable-dev-shm-usage',
// 						'--allow-pre-commit-input',
// 						'--in-process-gpu',
// 					]
// 				}); //  '--disable-gpu', '--disable-setuid-sandbox'

// 			// Running Lighthouse by custom options
// 			const options = {
// 				logLevel: 'info', 
// 				output: 'json', 
// 				port: chrome.port,
// 				formFactor: 'desktop', // 'desktop' or 'mobile'
// 				screenEmulation: screenEmulationMetrics.desktop,
// 				emulatedUserAgent: DESKTOP_USERAGENT, //MOTOG4_USERAGENT,
// 				skipAudits: [
// 					// Skip the h2 audit so it doesn't lie to us. See https://github.com/GoogleChrome/lighthouse/issues/6539
// 					'uses-http2',
// 					// There are always bf-cache failures when testing in headless. Reenable when headless can give us realistic bf-cache insights.
// 					'bf-cache',
// 				],
// 			};
// 			const runnerResult = await lighthouse(data.performance.url, options);

// 			// Send report to server
// 			const reportResponse = await fetch(`${SERVER_URL}/api/report/${UUID}/performance/${data.performance.pk}`, {
// 				method: 'POST',
// 				headers: {
// 					'User-Agent': USER_AGENT,
// 					'Content-Type': 'application/json'
// 				},
// 				body: runnerResult.report
// 			}).then((returnedResponse) => {
// 				console.log("Report has been forwarded http status", returnedResponse.status)
// 			}).catch((error) => {
// 				console.log(error)
// 			});

// 			// Kill chrome process
// 			await chrome.kill();

// 			// Wait 1 seconds before next request
// 			await new Promise(resolve => setTimeout(resolve, 1000));
// 		} else {
// 			// Wait 5 seconds before next request
// 			await new Promise(resolve => setTimeout(resolve, 10000));
// 		}
// 	} catch (error) {
// 		console.error(error);
// 		console.log('Wait for 10 seconds');
// 		// Wait 5 seconds before next request
// 		await new Promise(resolve => setTimeout(resolve, 10000));
// 	}
// }