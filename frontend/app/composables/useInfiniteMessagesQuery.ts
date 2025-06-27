import { useInfiniteQuery } from "@tanstack/vue-query";
import { getDocs, type Timestamp } from "firebase/firestore";
import type { ChatRepo, Message } from "~/utils/repos/chatRepo";

export default function (chatRepo: ChatRepo, conversationId: string) {
	const PAGE_SIZE = 30;

	const toast = useToast();

	const infQuery = useInfiniteQuery({
		queryKey: ["messages", chatRepo.userId, conversationId],
		initialPageParam: undefined,
		queryFn: async ({ pageParam }) => {
			const startAfterCreatedAt = pageParam as Timestamp | undefined;
			const q = chatRepo.queryMessages(conversationId, PAGE_SIZE, startAfterCreatedAt);
			const snapshot = await getDocs(q);
			return snapshot.docs;
		},
		select: (data) => ({
			pages: data.pages.map((docs) =>
				docs.map((doc) => {
					return { id: doc.id, ...doc.data() } as Message;
				}),
			),
			pageParams: data.pageParams,
			flatPages: data.pages.flatMap((docs) =>
				docs.map((doc) => {
					return { id: doc.id, ...doc.data() } as Message;
				}),
			),
		}),
		getNextPageParam: (lastPage) => {
			if (lastPage.length < PAGE_SIZE) return undefined; // No more pages
			const last = lastPage[lastPage.length - 1];

			if (!last) return undefined; // No documents in the last page
			return last.data().created_at;
		},
	});

	watch(infQuery.isError, (isError) => {
		if (!isError) return;

		const errorMessage =
			infQuery.error.value?.message ?? "An error occurred while fetching messages.";
		toast.add({
			color: "error",
			icon: "i-lucide-message-square-warning",
			title: "Failed to load messages",
			description: errorMessage,
		});
	});

	return infQuery;
}
