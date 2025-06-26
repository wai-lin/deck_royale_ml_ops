<script setup lang="ts">
import * as v from "valibot";
import type { FormSubmitEvent } from "@nuxt/ui";

const schema = v.object({
	playerTag: v.message(v.pipe(v.string(), v.nonEmpty()), "Enter a player tag"),
	input: v.message(v.pipe(v.string(), v.nonEmpty()), "Enter a message"),
});
type Schema = v.InferOutput<typeof schema>;
const state = reactive<Schema>({ playerTag: "", input: "" });

function onSubmit(event: FormSubmitEvent<Schema>) {
	console.log(event.data);
}
</script>

<template>
	<main class="mx-auto flex h-screen max-w-5xl flex-col gap-4">
		<header class="border-b-[0.5px] border-gray-600 p-4">
			<h3 class="text-xl font-bold">Deck Royale</h3>
			<p class="text-sm text-gray-500">Clash Royale deck builder.</p>
		</header>

		<section class="h-full flex-auto overflow-auto" />

		<UForm
			:schema="schema"
			:state="state"
			class="relative h-40 w-full flex-none p-4"
			@submit="onSubmit"
		>
			<UTextarea
				v-model="state.input"
				:maxrows="6"
				autoresize
				class="h-full w-full items-stretch"
			/>
			<UInput v-model="state.playerTag" placeholder="" :ui="{ base: 'peer' }">
				<label
					class="text-highlighted peer-focus:text-highlighted peer-placeholder-shown:text-dimmed pointer-events-none absolute -top-2.5 left-0 px-1.5 text-xs font-medium transition-all peer-placeholder-shown:top-1.5 peer-placeholder-shown:text-sm peer-placeholder-shown:font-normal peer-focus:-top-2.5 peer-focus:text-xs peer-focus:font-medium"
				>
					<span class="bg-default inline-flex px-1">Player Tag</span>
				</label>
			</UInput>
			<UButton type="submit" icon="i-lucide-send-horizontal" class="absolute top-6 right-6" />
		</UForm>
	</main>
</template>
