// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
	compatibilityDate: "2025-05-15",
	devtools: { enabled: true },
	future: {
		compatibilityVersion: 4,
	},
	css: ["~/assets/css/main.css"],
	modules: ["@nuxt/eslint", "@nuxt/ui", "@vueuse/nuxt"],
	devServer: {
		port: 3002,
	},
	runtimeConfig: {
		public: {
			apiBaseUrl: "",
			firebaseApiKey: "",
			firebaseAuthDomain: "",
			firebaseProjectId: "",
			firebaseStorageBucket: "",
			firebaseMessagingSenderId: "",
			firebaseAppId: "",
			firebaseMeasurementId: "",
		},
	},
	app: {
		head: {
			title: "Deck Royale",
		},
	},
});
