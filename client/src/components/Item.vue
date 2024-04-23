<script setup lang="ts">

const props = defineProps<{
  item_id: number
  cart_item_id: number
  click_counter: number
}>();

const emit = defineEmits<{
  (e: 'update:cart_item_id', value: number): void
  (e: 'update:click_counter', value: number): void
}>();

const newCartItem = () => {
  emit('update:cart_item_id', props.item_id);
  emit('update:click_counter', props.click_counter + 1);
}

</script>

<template>
    <div class="item">
      <i>
        <slot name="image"></slot>
      </i>
      <div class="item-info">
        <h4>
          <slot name="name"></slot>
        </h4>
        <h3>
          <slot name="price"></slot>
        </h3>
      </div>   
        <img class="cart-icon" src="./icons/add-cart.png" @click="newCartItem"/>
    </div>
  </template>

<style scoped>

:slotted(img) {
  width: 210px;
  height: 180px;
  border-radius: 0px 0px 10px 10px;
  box-shadow: 6px 6px #A7EEA2;
}

h3 {
  display: block;
}

h4 {
  font-weight: 500;
  margin-bottom: -10px;
  display: block;
  max-width: 150px;
}

.cart-icon {
  width: 30px;
  float: right;
  margin-top: -60px;
  padding: 5px;
  background-color: #eaeaea;
  border-radius: 5px;
  box-shadow: 1px 2px 2px #e0e0e0;
}

.cart-icon:hover{
  background-color: #A7EEA2;
  transition-duration: 0.4s;
}
</style>