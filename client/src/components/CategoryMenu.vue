<script setup lang="ts">
const categories = [
        {
            "id": 1,
            "image_id": "f3fbf57b118fa9",
            "name": "Bakery"
        },
        {
            "id": 2,
            "image_id": "b271afbefdc554",
            "name": "Entrees"
        },
        {
            "id": 3,
            "image_id": "eba73b2361fae3",
            "name": "Drinks"
        }
    ];
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