import { initializeApp } from "firebase/app";
import { initializeFirestore } from "firebase/firestore";

export default createGlobalState(() => {
	const env = useEnv();

	const app = initializeApp(env.firebaseConfig);
	const db = initializeFirestore(app, {});

	return { app, db };
});
