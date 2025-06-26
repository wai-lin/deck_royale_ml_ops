import { useMutation, useQueryClient } from "@tanstack/vue-query";
import * as v from "valibot";
import type { ChatRepo, PromptChatRequest } from "~/utils/repos/chatRepo";

export default function (chatRepo: ChatRepo) {
	const toast = useToast();

	const schema = v.object({
		input: v.message(v.pipe(v.string(), v.nonEmpty()), "Enter a message"),
	});
	type Schema = v.InferOutput<typeof schema>;
	const state = reactive<Schema>({ input: "" });

	const queryClient = useQueryClient();

	const mutation = useMutation({
		mutationFn: async (prompt: PromptChatRequest) => {
			return await chatRepo.promptChat({ ...prompt });
		},
		onSuccess: () => {
			state.input = "";
			queryClient.invalidateQueries({
				queryKey: ["messages"],
			});
		},
		onError: (err) => {
			const errorMessage = err?.message ?? "An error occurred while sending the message.";
			toast.add({
				color: "error",
				icon: "i-lucide-message-square-warning",
				title: "Failed to send message",
				description: errorMessage,
			});
		},
	});

	return { state, schema, mutation };
}
