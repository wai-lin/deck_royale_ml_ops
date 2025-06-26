<template>
	<div class="grid h-screen w-screen grid-cols-10 overflow-hidden">
		<aside class="col-span-2 flex h-screen flex-col gap-2 px-4">
			<header class="flex flex-none flex-col items-stretch gap-4">
				<div>
					<h3 class="text-xl font-bold">Deck Royale</h3>
					<p class="text-sm text-gray-500">Clash Royale deck builder.</p>
				</div>
				<!-- TODO: create new conversation -->
				<UButton label="New Conversation" class="justify-center" />
			</header>

			<nav class="flex flex-auto flex-col gap-2 overflow-y-auto">
				<UButton variant="soft" label="Conversations 1" />
				<UButton variant="ghost" label="Conversations 2" />
			</nav>
			<!-- Conversation List Here -->
		</aside>

		<main class="col-span-8 flex h-screen flex-col gap-4">
			<section class="h-full flex-auto overflow-auto px-8">
				<NuxtPage />
			</section>

			<section class="flex-none"></section>
		</main>
	</div>
</template>
