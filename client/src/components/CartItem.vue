<script setup lang="ts">
const props = defineProps<{
  unitPrice: number
  quantity: number
  item_id: number
  cart_item_id: number
  add_cart_item: number
  remove_cart_item: number
  delete_cart_item: number
}>()

const emit = defineEmits<{
  (e: 'update:cart_item_id', value: number): void
  (e: 'update:add_cart_item', value: number): void
  (e: 'update:remove_cart_item', value: number): void
  (e: 'update:delete_cart_item', value: number):void
}>();

const newCartItem = () => {
  emit('update:cart_item_id', props.item_id);
  emit('update:add_cart_item', props.add_cart_item + 1);
}

const removeCartItem = () => {
  emit('update:cart_item_id', props.item_id);
  emit('update:remove_cart_item', props.remove_cart_item + 1);
}

const deleteCartItem = () => {
  emit('update:cart_item_id', props.item_id);
  emit('update:delete_cart_item', props.delete_cart_item + 1);
}
</script>

<template>
  <div class="cart-item">
    <i>
      <slot name="cart-image"></slot>
    </i>
    <div class="cart-item-info">
      <h4 class="cart-name">
        <slot name="cart-name"></slot>
      </h4>
      <h5 class="cart-category">
        <slot name="cart-category"></slot>
      </h5>
      <h5 class="cart-unit-price">Price per serving: {{ unitPrice.toFixed(2) }}</h5>
      <h3 class="cart-item-total-price">
        {{ (unitPrice * quantity).toFixed(2) }}
      </h3>      
    </div> 
    <div class="cart-item-buttons">
        <button class="cart-delete" @click="deleteCartItem">x</button>
        <button class="cart-remove" @click="removeCartItem">-</button>
        <input type="text" class="cart-quantity" readonly="true" disabled="true" :value="quantity" />
        <button class="cart-add" @click="newCartItem">+</button>
       
    </div>   
  </div>
</template>

<style scoped>
:slotted(img) {
  width: 64px;
  height: 64px;
  margin-left: 45px;
  display: block;
  border-radius: 3px;
}
.cart-item {
    margin-top: 40px;
    margin-right: -16px;
    margin-bottom: 20px;
}

.cart-name {
  margin-right: 45px;
  float: right;
  display: block;
  margin-top: -63px;
  font-weight: 500;
}

.cart-category, .cart-unit-price {
  margin-right: 45px;
  float: right;
  display: block;
  margin-top: -39px;
  font-weight: 500;
}

.cart-unit-price {
  margin-top: -16px;
  font-size: 12px;
  color: gray;
}

.cart-item-buttons {
    display: flex;
    justify-content: left;
    margin-top: 20px;
    margin-left: 45px;

}

.cart-item-total-price {
    float: right;
    margin-right: -130px;
    font-size: 16px;
    margin-top: 24px;
}

input {
    text-align: center;
    max-width: 60px;
    font-weight: 900;
    border: none;
    background-color: white;
    max-height: 26px;
    margin-right: 5px;
    border-radius: 3px;
}

button {
    background: #A7EEA2;
    border: none;
    margin-right: 5px;
    text-align: center;
    width: 26px;
    height: 26px;
    font-weight: 900;
    border-radius: 3px;
}

button:hover {
    transition-duration: 0.4s;
    background: linear-gradient(
    to top,
    rgba(255, 255, 255, 0.15),
    rgba(255, 255, 255, 0.15)
  ) #A7EEA2;
}

</style>
