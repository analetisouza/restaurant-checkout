<script setup lang="ts">
import CategoryMenu from './components/CategoryMenu.vue';
import Item from './components/Item.vue';
</script>

<template>
  <h1>Good night! Ready to order?</h1>
  <header/>
  <CategoryMenu/>
  <Item/>
</template>

<style scoped>

h1 {
  font-weight: bold;
  font-size: 44px;
  display: inline;
  margin-top: 40px;
  width: 360px;
  line-height: 1.2;
}
</style>
