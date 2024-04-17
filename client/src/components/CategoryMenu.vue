<script setup lang="ts">
defineProps<{
    categories: Record<string, any>[]
}>()

</script>

<template>
    <div class="category-menu">
        <h3>Categories</h3>
        <li v-for="category in categories">
            <h4>{{ category.name }}</h4>
        </li>
    </div>
</template>

<style scoped>

h3 {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 30px;
}

h4 { 
    font-size: 16px;
    margin-bottom: 10px;
    font-weight: 500;
}
.category-menu {
    float: left; 
    display: inline;
}
.category-menu li {
    list-style-type: none;
}

</style>