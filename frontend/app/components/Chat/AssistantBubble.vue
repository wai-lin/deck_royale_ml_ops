<script setup lang="ts">
import type { Message } from "~/utils/repos/chatRepo";

const compId = useId();

const { role, content, evaluation } = defineProps<Message>();
if (role !== "assistant") {
	throw new Error("Invalid role for DeckResponse component");
}
</script>

<template>
	<div class="flex items-start justify-start gap-4">
		<UAvatar icon="i-lucide-bot-message-square" size="xl" />

		<!-- Assistant Bubble -->
		<div class="max-w-lg rounded-lg bg-neutral-500 p-6 text-neutral-200 shadow-md">
			<h2 class="mb-4 text-2xl font-bold">
				Deck: <span class="text-primary-300">{{ content.deck_name }}</span>
			</h2>
			<p class="mb-4"><strong>Average Elixir Cost:</strong> {{ content.average_elixir_cost }}</p>

			<!-- Cards -->
			<div class="mb-4 grid grid-cols-4 gap-2">
				<div
					v-for="card in content.cards"
					:key="`${compId}-${card.id}`"
					class="flex flex-col items-center space-y-2"
				>
					<img :src="card.iconUrls.medium" :alt="card.name" class="size-32 object-contain" />
					<span class="text-sm font-medium">{{ card.name }}</span>
				</div>
			</div>

			<div class="prose max-w-none">
				<p>
					{{ content.comment }}
				</p>
			</div>

			<!-- Evaluation Section -->
			<div class="mt-6 border-t border-neutral-400 pt-4 text-neutral-300">
				<h3 class="mb-2 text-xl font-semibold">Evaluation</h3>
				<ul class="space-y-1">
					<li><strong>Overall:</strong> {{ evaluation.overall }}</li>
					<li><strong>Defense:</strong> {{ evaluation.defense }}</li>
					<li><strong>Attack:</strong> {{ evaluation.attack }}</li>
					<li><strong>Synergy:</strong> {{ evaluation.synergy }}</li>
					<li><strong>Versatility:</strong> {{ evaluation.versatility }}</li>
					<li><strong>Average Elixir:</strong> {{ evaluation.avg_elixir }}</li>
					<li><strong>Difficulty:</strong> {{ evaluation.difficulty }}</li>
					<li><strong>Deck Type:</strong> {{ evaluation.deck_type }}</li>
				</ul>
				<p class="mt-2">{{ evaluation.comments }}</p>
			</div>
		</div>
	</div>
</template>
