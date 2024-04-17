<script setup lang="ts">
import menu from './components/menu.json'
import CategoryMenu from './components/CategoryMenu.vue';
import Item from './components/Item.vue';

function getDayPeriod(): string {
  const now = new Date();
  const hour = now.getHours();
  const periods = [{"time": "morning", "condition": hour >= 6 && hour < 12}, 
                   {"time": "afternoon", "condition": hour >= 12 && hour < 18}, 
                   {"time": "night", "condition": hour >= 18 || hour < 6}]
  let currentPeriod = "";

  for (const period of periods) {
    if (period.condition)
      currentPeriod = period.time;
  }
  return currentPeriod;
}

function getImage(image_id: string): string {
  return new URL(`./components/images/${image_id}.jpg`, import.meta.url).href;
}

</script>

<template>
  <header>
  <h1>Good {{ getDayPeriod() }}! Ready to order?</h1>
  </header>
  <CategoryMenu :categories="menu.categories" />
  <div class="item-wrapper">
  <li v-for="item in menu.items">
    <Item class="item">
      <template #image> <img :src="getImage(item.image_id)"/> </template>
      <template #name> {{ item.name }}</template>
      <template #price> {{ item.price.toFixed(2) }}</template>
    </Item>
  </li>
  </div>
</template>

<style scoped>

h1 {
  font-weight: bold;
  font-size: 44px;
  display: block;
  margin-top: 40px;
  width: 360px;
  line-height: 1.2;
}

li {
  list-style-type: none;
}

.item-wrapper{
  margin-top: 42px;
  margin-left: 240px;
  display: grid;
  grid-template-columns: 210px 210px 210px;
  grid-column-gap: 36px;
  grid-row-gap: 30px;
}

.item {
  width: fit-content;
}

</style>
