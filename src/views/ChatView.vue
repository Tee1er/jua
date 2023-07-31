<script>
import TopBar from "../components/TopBar.vue"
import MachineCard from "../components/MachineCard.vue"
import Navbar from "../components/Navbar.vue"

export default {
    components: {
        TopBar,
        MachineCard,
        Navbar
    },
}
</script>

<template>
    <div class="flex flex-col">
        <div class="p-8">
            <TopBar></TopBar>

            <h2 class="mt-8 text-2xl font-semibold text-gray-700">Your device</h2>



        </div>
        <Navbar></Navbar>
    </div>
</template>