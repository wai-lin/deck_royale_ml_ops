<template>
	<NuxtLoadingIndicator />
	<NuxtRouteAnnouncer />
	<UApp
		:toaster="{
			position: 'top-center',
			duration: 5000,
		}"
	>
		<NuxtLayout>
			<NuxtPage />
		</NuxtLayout>
	</UApp>
</template>
