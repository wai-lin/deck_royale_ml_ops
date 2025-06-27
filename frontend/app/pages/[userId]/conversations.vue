<script setup lang="ts">
import { ChatRepo } from "~/utils/repos/chatRepo";

const route = useRoute();
const { db } = useFirebaseInstance();

if (typeof route.params.userId !== "string") {
	throw new Error("Invalid userId parameter");
}

const userId = route.params.userId;
function getConvoUrl(conversationId: string) {
	return `/${userId}/conversations/${conversationId}`;
}

const userTag = computed(() => `#${route.params.userId}`);
const chatRepo = new ChatRepo(db, userTag.value);
const { data, isFetching } = useInfiniteConversationsQuery(chatRepo);
</script>

<template>
	<div class="grid h-screen w-screen grid-cols-10 overflow-hidden">
		<aside class="col-span-2 flex h-screen flex-col gap-2 bg-neutral-800 px-4 pt-4">
			<header class="flex flex-none flex-col items-stretch gap-4">
				<div>
					<h3 class="text-xl font-bold">Deck Royale</h3>
					<p class="text-sm text-gray-500">Clash Royale deck builder.</p>
				</div>

				<ChatNewConversationBtn />
			</header>

			<nav v-if="isFetching" class="flex flex-auto flex-col gap-2 overflow-y-auto">
				<UButton variant="soft" label="Loading..." loading />
			</nav>

			<!-- Conversation List -->
			<nav class="flex flex-auto flex-col gap-2 overflow-y-auto">
				<UButton
					v-for="conv in data?.flatPages ?? []"
					:key="conv.id"
					variant="soft"
					:label="conv?.title ?? '-'"
					:to="getConvoUrl(conv.id)"
				/>
			</nav>
		</aside>

		<main class="col-span-8 flex h-screen flex-col gap-4 pt-4">
			<NuxtPage />
		</main>
	</div>
</template>
