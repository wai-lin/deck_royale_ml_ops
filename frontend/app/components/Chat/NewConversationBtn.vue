<script setup lang="ts">
import type * as v from "valibot";
import type { FormSubmitEvent } from "@nuxt/ui";
import { ChatRepo } from "~/utils/repos/chatRepo";

const config = useRuntimeConfig().public;
const route = useRoute();

if (typeof route.params.userId !== "string") {
	throw new Error("Invalid userId parameter");
}
const userTag = computed(() => `#${route.params.userId}`);

const { db } = useFirebaseInstance();

const chatRepo = new ChatRepo(db, userTag.value, config.apiBaseUrl);
const { state, schema, mutation } = useCreateConversationMutation(chatRepo);
type Schema = v.InferOutput<typeof schema>;

async function onSubmit(event: FormSubmitEvent<Schema>) {
	mutation.mutate(event.data.title);
}
</script>

<template>
	<UPopover>
		<UButton label="New Conversation" class="justify-center" />

		<template #content>
			<UForm
				:schema="schema"
				:state="state"
				:disabled="mutation.isPending.value"
				class="flex items-end gap-4 p-4"
				@submit="onSubmit"
			>
				<UFormField label="Title" name="title">
					<UInput v-model="state.title" placeholder="Give conversation title" />
				</UFormField>

				<UButton
					type="submit"
					:loading="mutation.isPending.value"
					icon="i-lucide-send-horizontal"
				/>
			</UForm>
		</template>
	</UPopover>
</template>
