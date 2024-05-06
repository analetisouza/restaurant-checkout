<script setup lang="ts">
import { watch, ref } from 'vue'
import axios from 'axios'
import CategoryMenu from '../components/CategoryMenu.vue'
import Item from '../components/Item.vue'
import CartItem from '../components/CartItem.vue'
import { createCategoryMenuStore } from '@/stores/categoryMenu'
import { useRouter } from 'vue-router'

function getDayPeriod(): string {
  const now = new Date()
  const hour = now.getHours()
  const periods = [
    { time: 'morning', condition: hour >= 6 && hour < 12 },
    { time: 'afternoon', condition: hour >= 12 && hour < 18 },
    { time: 'night', condition: hour >= 18 || hour < 6 }
  ]
  let currentPeriod = ''

  for (const period of periods) {
    if (period.condition) currentPeriod = period.time
  }
  return currentPeriod
}

function getImage(image_id: string): string {
  return new URL(`../../../server/database/data/images/${image_id}.jpg`, import.meta.url).href
}

const categoriesList: Record<string, boolean> = { All: true }
for (const category of categories) {
  categoriesList[category.name] = false
}

const useCategoryMenuStore = createCategoryMenuStore(categoriesList)
const categoryMenuStore = useCategoryMenuStore()

const items = ref([])
const cart = ref([])
const cart_id = ref(0)
const cart_item_id = ref(0)
const add_cart_item = ref(0)
const remove_cart_item = ref(0)
const delete_cart_item = ref(0)

watch(
  categoryMenuStore,
  async () => {
    for (const category in categoryMenuStore.categoryMenuState) {
      if (categoryMenuStore.categoryMenuState[category] === true) {
        try {
          items.value = await axios
            .get(`http://127.0.0.1:8000/items/?category_filter=${category}`)
            .then((res) => res.data)
        } catch (error) {
          console.log(error)
        }
      }
    }
  },
  { immediate: true }
)

watch(
  add_cart_item,
  async () => {
    if (cart_id.value === 0) {
      cart_id.value = await axios.post('http://127.0.0.1:8000/cart/').then((res) => res.data)
    } else {
      await axios
        .put(
          `http://127.0.0.1:8000/cart/${cart_id.value}/?operation=add&item_id=${cart_item_id.value}`
        )
        .then((res) => res.data)
      cart.value = await axios
        .get(`http://127.0.0.1:8000/cart/${cart_id.value}/`)
        .then((res) => res.data)
    }
  },
  { immediate: true }
)

watch(remove_cart_item, async () => {
  await axios
    .put(
      `http://127.0.0.1:8000/cart/${cart_id.value}/?operation=remove&item_id=${cart_item_id.value}`
    )
    .then((res) => res.data)
  cart.value = await axios
    .get(`http://127.0.0.1:8000/cart/${cart_id.value}/`)
    .then((res) => res.data)
  cart_item_id.value = 0
})

watch(delete_cart_item, async () => {
  await axios
    .delete(`http://127.0.0.1:8000/cart/${cart_id.value}/?item_id=${cart_item_id.value}`)
    .then((res) => res.data)
  cart.value = await axios
    .get(`http://127.0.0.1:8000/cart/${cart_id.value}/`)
    .then((res) => res.data)
  cart_item_id.value = 0
})

const totalCart = () => {
  let sumTotalCart = 0
  for (const cartItem of cart.value) {
    sumTotalCart += cartItem.price * cartItem.quantity
  }
  return sumTotalCart
}
const router = useRouter()
const gotoPayment = () =>
  router.push({
    name: 'payment',
    params: { cartId: cart_id.value },
    state: { orderPrice: totalCart() }
  })
</script>

<script async lang="ts">
const categories = await axios.get('http://127.0.0.1:8000/categories/').then((res) => res.data)
</script>

<template>
  <header>
    <h1>Good {{ getDayPeriod() }}! Ready to order?</h1>
  </header>
  <CategoryMenu :categoryMenuStore="categoryMenuStore" />
  <div class="item-wrapper">
    <li v-for="item in items">
      <Item
        class="item"
        :item_id="item.id"
        v-model:cart_item_id="cart_item_id"
        v-model:add_cart_item="add_cart_item"
      >
        <template #image> <img :src="getImage(item.image_id)" /> </template>
        <template #name> {{ item.name }}</template>
        <template #price> {{ item.price.toFixed(2) }}</template>
      </Item>
    </li>
  </div>
  <div class="cart-wrapper">
    <h3>Cart</h3>
    <li v-for="cart_item in cart">
      <CartItem
        :unitPrice="cart_item.price"
        :quantity="cart_item.quantity"
        v-model:item_id="cart_item.item_id"
        v-model:cart_item_id="cart_item_id"
        v-model:add_cart_item="add_cart_item"
        v-model:remove_cart_item="remove_cart_item"
        v-model:delete_cart_item="delete_cart_item"
      >
        <template #cart-image> <img :src="getImage(cart_item.image_id)" /> </template>
        <template #cart-name> {{ cart_item.item_name }}</template>
        <template #cart-category> {{ cart_item.category_name }}</template>
      </CartItem>
    </li>
    <div class="cart-end"></div>
    <div class="total-wrapper">
      <h5>Total</h5>
      <h4>{{ totalCart().toFixed(2) }}</h4>
      <button @click="gotoPayment">Continue</button>
      <router-view></router-view>
    </div>
  </div>
</template>

<style scoped>
h1 {
  font-weight: bold;
  font-size: 44px;
  display: block;
  margin-top: -10px;
  width: 360px;
  line-height: 1.2;
}

h4 {
  margin-left: 45px;
  margin-bottom: 32px;
  font-size: 20px;
}

h5 {
  margin-left: 45px;
  margin-bottom: -20px;
  font-size: 16px;
  font-weight: 500;
}

li {
  list-style-type: none;
}

.item-wrapper {
  margin-top: 46px;
  margin-left: 210px;
  display: grid;
  grid-template-columns: 210px 210px 210px;
  grid-column-gap: 36px;
  grid-row-gap: 24px;
}

.item {
  width: fit-content;
}

.cart-wrapper {
  background-color: #eaeaea;
  height: 100vh;
  width: 25%;
  position: fixed;
  z-index: 2;
  top: 0;
  right: 0;
  overflow-y: scroll;
}

.cart-wrapper h3 {
  padding-top: 30px;
  padding-left: 45px;
}

.cart-end {
  height: 80px;
}

::-webkit-scrollbar {
  background: #eaeaea;
}

.total-wrapper {
  z-index: 1;
  max-height: 160px;
  width: 25%;
  background-color: rgb(234, 234, 234, 0.85);
  position: fixed;
  right: 0;
  bottom: 0;
}

.total-wrapper button {
  float: right;
  margin-top: -75px;
  margin-right: 45px;
  background: #a7eea2;
  font-size: 16px;
  font-weight: 550;
  border: none;
  border-radius: 4px;
  padding: 10px;
  box-shadow: 1px 2px 2px #e0e0e0;
}

.total-wrapper button:hover {
  transition-duration: 0.4s;
  background: linear-gradient(to top, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.15)) #a7eea2;
}
</style>
