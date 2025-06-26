import {
	collection,
	doc,
	limit,
	orderBy,
	query,
	startAfter,
	type DocumentSnapshot,
	type Firestore,
} from "firebase/firestore";

export class ChatRepo {
	private readonly userRef: ReturnType<typeof collection>;
	private readonly convosRef: ReturnType<typeof collection>;

	constructor(
		private readonly db: Firestore,
		private readonly userId: string,
	) {
		this.userRef = collection(this.db, "users", this.userId);
		this.convosRef = collection(this.userRef, "conversations");
	}

	queryConversations(pageSize: number, startAfterDoc?: DocumentSnapshot) {
		let q = query(this.convosRef, orderBy("updated_at", "desc"), limit(pageSize));
		if (startAfterDoc) q = query(q, startAfter(startAfterDoc));
		return q;
	}

	getConversationDocRef(conversationId: string) {
		return doc(this.convosRef, conversationId);
	}

	getMessagesCollectionRef(conversationId: string) {
		const convoDocRef = this.getConversationDocRef(conversationId);
		return collection(convoDocRef, "messages");
	}

	queryMessages(conversationId: string, pageSize: number, startAfterDoc?: DocumentSnapshot) {
		const messagesRef = this.getMessagesCollectionRef(conversationId);
		let q = query(messagesRef, orderBy("created_at", "asc"), limit(pageSize));
		if (startAfterDoc) q = query(q, startAfter(startAfterDoc));
		return q;
	}
}
