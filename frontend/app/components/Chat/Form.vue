<script setup lang="ts">
import type * as v from "valibot";
import type { FormSubmitEvent } from "@nuxt/ui";
import { ChatRepo } from "~/utils/repos/chatRepo";

const config = useRuntimeConfig().public;
const route = useRoute();

if (typeof route.params.conversationId !== "string") {
	throw new Error("Invalid conversationId parameter");
}
const conversationId = computed(() => route.params.conversationId as string);

if (typeof route.params.userId !== "string") {
	throw new Error("Invalid userId parameter");
}
const userId = computed(() => route.params.userId as string);
const userTag = computed(() => `#${userId.value}`);

const { db } = useFirebaseInstance();

const chatRepo = new ChatRepo(db, userId.value, config.apiBaseUrl);
const { schema, state, mutation } = useChatMutation(chatRepo);
type Schema = v.InferOutput<typeof schema>;

function onSubmit(event: FormSubmitEvent<Schema>) {
	const data = event.data;
	mutation.mutate({
		conversation_id: conversationId.value,
		player_id: userTag.value,
		message: data.input,
	});
}
</script>

<template>
	<UForm
		:schema="schema"
		:state="state"
		:disabled="mutation.isPending.value"
		class="relative h-40 w-full p-4"
		@submit="onSubmit"
	>
		<UTextarea v-model="state.input" :maxrows="6" autoresize class="h-full w-full items-stretch" />
		<UButton
			type="submit"
			icon="i-lucide-send-horizontal"
			:loading="mutation.isPending.value"
			class="absolute top-6 right-6"
		/>
	</UForm>
</template>
