import {
	addDoc,
	collection,
	doc,
	limit,
	orderBy,
	query,
	serverTimestamp,
	startAfter,
	type Firestore,
	type Timestamp,
} from "firebase/firestore";

export type Conversation = {
	id: string;
	title: string;
	created_at: Timestamp;
	updated_at: Timestamp;
};

export type Message =
	| {
			id: string;
			role: "user";
			content: string;
			evaluation: null;
			created_at: Timestamp;
			updated_at: Timestamp;
	  }
	| {
			id: string;
			role: "assistant";
			content: {
				deck_name: string;
				average_elixir_cost: number;
				comment: string;
				cards: Array<{
					id: number;
					elixirCost: number;
					maxEvolutionLevel: number;
					maxLevel: number;
					name: string;
					rarity: string;
					iconUrls: {
						medium: string;
						evolutionMedium?: string | null;
					};
				}>;
			};
			evaluation: {
				overall: number;
				defense: number;
				attack: number;
				synergy: number;
				versatility: number;
				avg_elixir: number;
				difficulty: number;
				deck_type: string;
				comments: string;
			};
			created_at: Timestamp;
			updated_at: Timestamp;
	  };

export type PromptChatRequest = {
	player_id: string;
	conversation_id: string;
	message: string;
};

export type PromptChatResponse = {
	agent_response_id: string;
	response: Message["role"] extends "assistant" ? Message["content"] : never;
};

export class ChatRepo {
	private readonly userRef: ReturnType<typeof doc>;
	private readonly convosRef: ReturnType<typeof collection>;

	constructor(
		private readonly db: Firestore,
		public readonly userId: string,
		private readonly apiBaseUrl: string = "",
	) {
		const usersCol = collection(this.db, "users");
		this.userRef = doc(usersCol, this.userId);
		this.convosRef = collection(this.userRef, "conversations");
	}

	async createConversation(title: string) {
		const now = serverTimestamp();
		try {
			const docRef = await addDoc(this.convosRef, {
				title,
				created_at: now,
				updated_at: now,
			});
			console.log("Conversation created with ID:", docRef.id);
			return docRef;
		} catch (error) {
			console.error("Failed to create conversation:", error);
			throw error;
		}
	}

	async promptChat(req: PromptChatRequest) {
		return await $fetch<PromptChatResponse>("/chat", {
			baseURL: this.apiBaseUrl,
			method: "post",
			body: req,
		});
	}

	queryConversations(pageSize: number, startAfterUpdatedAt?: Timestamp) {
		let q = query(this.convosRef, orderBy("updated_at", "desc"), limit(pageSize));
		if (startAfterUpdatedAt) q = query(q, startAfter(startAfterUpdatedAt));
		return q;
	}

	getConversationDocRef(conversationId: string) {
		return doc(this.convosRef, conversationId);
	}

	getMessagesCollectionRef(conversationId: string) {
		const convoDocRef = this.getConversationDocRef(conversationId);
		return collection(convoDocRef, "messages");
	}

	queryMessages(conversationId: string, pageSize: number, startAfterCreatedAt?: Timestamp) {
		const messagesRef = this.getMessagesCollectionRef(conversationId);
		let q = query(messagesRef, orderBy("created_at", "asc"), limit(pageSize));
		if (startAfterCreatedAt) q = query(q, startAfter(startAfterCreatedAt));
		return q;
	}
}
