import { useMutation, useQueryClient } from "@tanstack/vue-query";
import * as v from "valibot";
import type { ChatRepo } from "~/utils/repos/chatRepo";

export default function (chatRepo: ChatRepo) {
	const toast = useToast();

	const schema = v.object({
		title: v.pipe(
			v.string(),
			v.minLength(1, "Title is required"),
			v.maxLength(100, "Title must be less than 100 characters"),
		),
	});
	type Schema = v.InferOutput<typeof schema>;
	const state = reactive<Schema>({ title: "" });

	const queryClient = useQueryClient();

	const mutation = useMutation({
		mutationFn: async (title: string) => {
			return await chatRepo.createConversation(title);
		},
		onSuccess: () => {
			state.title = "";
			queryClient.invalidateQueries({
				queryKey: ["conversations"],
			});
		},
		onError: (err) => {
			const errorMessage = err?.message ?? "An error occurred while creating the conversation.";
			toast.add({
				color: "error",
				icon: "i-lucide-message-square-warning",
				title: "Failed to create conversation",
				description: errorMessage,
			});
		},
	});

	return { state, schema, mutation };
}
