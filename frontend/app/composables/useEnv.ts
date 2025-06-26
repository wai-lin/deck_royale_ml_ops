export default function () {
	const conf = useRuntimeConfig().public;

	return {
		apiBaseUrl: conf.apiBaseUrl,
		firebaseConfig: {
			apiKey: conf.firebaseApiKey,
			authDomain: conf.firebaseAuthDomain,
			projectId: conf.firebaseProjectId,
			storageBucket: conf.firebaseStorageBucket,
			messagingSenderId: conf.firebaseMessagingSenderId,
			appId: conf.firebaseAppId,
			measurementId: conf.firebaseMeasurementId,
		},
	};
}
