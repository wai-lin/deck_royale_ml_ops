<script setup lang="ts">
import type { FormSubmitEvent } from "@nuxt/ui";

const router = useRouter();

const state = reactive({
	playerTag: "",
});
function onSubmit(event: FormSubmitEvent<{ playerTag: string }>) {
	const data = event.data;
	const playerTag = data.playerTag.replace("#", "");
	router.push(`/${playerTag}/conversations`);
}
</script>

<template>
	<main class="container mx-auto grid h-screen place-items-center p-4">
		<UCard>
			<template #header>
				<h2 class="text-xl font-bold">Deck Royale</h2>
				<p class="text-neutral-500">Personalize your Clash Royale deck building experience.</p>
			</template>

			<UForm :state="state" class="flex gap-4" @submit="onSubmit">
				<UInput v-model="state.playerTag" placeholder="" :ui="{ base: 'peer' }" class="w-full">
					<label
						class="text-highlighted peer-focus:text-highlighted peer-placeholder-shown:text-dimmed pointer-events-none absolute -top-2.5 left-0 px-1.5 text-xs font-medium transition-all peer-placeholder-shown:top-1.5 peer-placeholder-shown:text-sm peer-placeholder-shown:font-normal peer-focus:-top-2.5 peer-focus:text-xs peer-focus:font-medium"
					>
						<span class="bg-default inline-flex px-1">Player Tag</span>
					</label>
				</UInput>

				<UButton type="submit" label="Continue" />
			</UForm>
		</UCard>
	</main>
</template>
