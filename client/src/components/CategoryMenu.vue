<script setup lang="ts">
const props = defineProps<{
    categories: Record<string, any>[]
}>()

import { createCategoryMenuStore }  from '@/stores/categoryMenu';

const categoriesList: Record<string, boolean> = {"All": true};
for (const category of props.categories){
    categoriesList[category.name] = false;
}

const useCategoryMenuStore = createCategoryMenuStore(categoriesList);
const categoryMenuStore = useCategoryMenuStore();


function checkCategoryMenuState(newState: string) {
    for (const category in categoryMenuStore.categoryMenuState) 
        categoryMenuStore.categoryMenuState[category] = newState === category ? true : false;
    }  

</script>

<template>
    <div class="category-menu">
        <h3>Categories</h3>
        <li v-for="state, category in categoryMenuStore.categoryMenuState" :key="category">
            <button @click="checkCategoryMenuState(category)" :class="{active: state}">{{ category }}</button>
        </li>
    </div>
</template>

<style scoped>

h3 {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 30px;
}

button { 
    font-size: 18px;
    margin-bottom: 12px;
    font-weight: 500;
    background: none;
    border: none;
    outline: none;
    box-shadow: none;
    padding: 6px 12px 6px 0px;
    border-left: 0px solid #A7EEA2;
    transition: border-left 0.4s ease-in;

}

button:hover, button.active {
    background: #A7EEA2;
    border-radius: 0px 5px 5px 0px;
    border-left: 40px solid #A7EEA2;
    box-shadow: 1px 1px 1px #e0e0e0;
}

.category-menu {
    float: left; 
    display: inline;
}
.category-menu li {
    list-style-type: none;
}

</style>