import { useInfiniteQuery } from "@tanstack/vue-query";
import { getDocs, type Timestamp } from "firebase/firestore";
import type { ChatRepo, Conversation } from "~/utils/repos/chatRepo";

export default function (chatRepo: ChatRepo) {
	const PAGE_SIZE = 100;

	const toast = useToast();

	const infQuery = useInfiniteQuery({
		queryKey: ["conversations", chatRepo.userId],
		initialPageParam: undefined,
		queryFn: async ({ pageParam }) => {
			const startAfterUpdatedAt = pageParam as Timestamp | undefined;
			const q = chatRepo.queryConversations(PAGE_SIZE, startAfterUpdatedAt);
			const snapshot = await getDocs(q);
			return snapshot.docs;
		},
		select: (data) => ({
			pages: data.pages.map((docs) =>
				docs.map((doc) => {
					return { id: doc.id, ...doc.data() } as Conversation;
				}),
			),
			pageParams: data.pageParams,
			flatPages: data.pages.flatMap((docs) =>
				docs.map((doc) => {
					return { id: doc.id, ...doc.data() } as Conversation;
				}),
			),
		}),
		getNextPageParam: (lastPage) => {
			if (lastPage.length < PAGE_SIZE) return undefined; // No more pages
			const last = lastPage[lastPage.length - 1];

			if (!last) return undefined; // No documents in the last page
			return last.data().updated_at;
		},
	});

	watch(infQuery.isError, (isError) => {
		if (!isError) return;

		const errorMessage =
			infQuery.error.value?.message ?? "An error occurred while fetching conversations.";
		toast.add({
			color: "error",
			icon: "i-lucide-message-square-warning",
			title: "Failed to load conversations",
			description: errorMessage,
		});
	});

	return infQuery;
}
