import fetch from 'node-fetch';
import amqp from 'amqplib';

// Load lighthouse and chrome-launcher to setup lighthouse locally
import lighthouse from 'lighthouse';
import chromeLauncher from 'chrome-launcher';

let UUID = process.env.UUID;
let BACKEND_URL = process.env.BACKEND_URL;
const SECRET_KEY = process.env.SECRET_KEY;
const CELERY_BROKER_URL = process.env.CELERY_BROKER_URL;
const USER_AGENT = 'fromedwin bot lighthouse worker';

// Request performance object entrypoint
let url = `${BACKEND_URL}/api/request/${UUID}/performance`

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
			// const args = message[0];
			const kwargs = message[1];

			// If message come from scheduler we verify if the report is still needed
			// This avoid to run useless task if multiple message were queued
			if (kwargs.source == 'scheduler') {

				let skip_run = false;
				console.log(`Checking if report is still needed for ${kwargs.url}`);
				await fetch(`${BACKEND_URL}/api/report/${SECRET_KEY}/performance/${kwargs.id}`, {
					method: 'GET',
					headers: {
						'User-Agent': USER_AGENT,
					}
				}).then(async (returnedResponse) => {
					// Get body as json
					const data = await returnedResponse.json();

					console.log("Report has been fetched", data);
					const now = new Date();
					const goodIfBefore = new Date(now.getTime() - data.LIGHTHOUSE_SCRAPE_INTERVAL_MINUTES * 60000);
					const lastReportDate = new Date(data.last_report_date);

					if (lastReportDate > goodIfBefore) {
						// Acknowledge the message as it is not needed
						console.log(`No need to re-run ${kwargs.url}, a report is already available.`);
						skip_run = true;
						// wait 400 ms to avoid looping too fast
						await new Promise(resolve => setTimeout(resolve, 400));
						channel.ack(msg);
					} else {
						console.log(`Last report is too old (${lastReportDate}), re-running ${kwargs.url}`);
					}
				}).catch((error) => {
					console.error(error)
				});
				if (skip_run) {
					return;
				}
			}

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
			const reportResponse = await fetch(`${BACKEND_URL}/api/report/${SECRET_KEY}/performance/${kwargs.id}`, {
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
