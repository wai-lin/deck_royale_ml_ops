<script setup lang="ts">
import { ChatRepo } from "~/utils/repos/chatRepo";

const route = useRoute();
const { db } = useFirebaseInstance();

if (typeof route.params.userId !== "string") {
	throw new Error("Invalid userId parameter");
}
if (typeof route.params.conversationId !== "string") {
	throw new Error("Invalid conversationId parameter");
}

const conversationId = route.params.conversationId;

const userTag = computed(() => `#${route.params.userId}`);
const chatRepo = new ChatRepo(db, userTag.value);

const { data, isFetching } = useInfiniteMessagesQuery(chatRepo, conversationId);

const msgContainerRef = useTemplateRef<HTMLElement>("msgContainerRef");
function scrollToBottom() {
	if (!msgContainerRef.value) return;
	msgContainerRef.value.scrollTo({
		top: msgContainerRef.value.scrollHeight,
		behavior: "smooth",
	});
}
onMounted(() => setTimeout(() => scrollToBottom(), 500));
watch(
	() => data.value?.flatPages,
	() => setTimeout(() => scrollToBottom(), 500),
	{ deep: true },
);
</script>

<template>
	<div v-if="isFetching" class="absolute inset-x-0 top-8 z-10 flex items-center justify-center">
		<UAlert
			title="Loading conversation..."
			description="This may take a while if the conversation is large."
			class="w-2/5"
		/>
	</div>
	<div
		v-if="data?.flatPages.length === 0"
		class="grid h-full flex-auto place-items-center text-neutral-300"
	>
		There's no conversation here.
	</div>
	<template v-else>
		<section ref="msgContainerRef" class="h-full flex-auto space-y-8 overflow-auto px-8">
			<div v-for="message in data?.flatPages ?? []" :key="message.id">
				<ChatUserBubble v-if="message.role === 'user'">{{ message.content }}</ChatUserBubble>
				<ChatAssistantBubble v-else-if="message.role === 'assistant'" v-bind="message" />
			</div>
		</section>
	</template>

	<ChatForm />
</template>
