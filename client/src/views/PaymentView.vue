<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import type { AxiosResponse } from 'axios'

const orderPrice = Number(history.state.orderPrice).toFixed(2)
const route = useRoute()
const router = useRouter()

const cardType = ref('')
const cardNumber = ref('')
const securityCode = ref('')
const expirationMonth = ref('')
const expirationYear = ref('')

const now = new Date()
const month = String(now.getMonth() + 1).padStart(2, '0')
const year = String(now.getFullYear())

const formatCardNumber = () => {
  let formattedCardNumber: string = ''
  for (const digit of cardNumber.value.replaceAll(' ', '').split('')) {
    formattedCardNumber += digit
    if (formattedCardNumber.split(' ').slice(-1)[0].length == 4) formattedCardNumber += ' '
  }
  cardNumber.value = formattedCardNumber
}

const validateDigit = (event: Event) => {
  const key = event.which ? event.which : event.keyCode
  if (!((key > 95 && key < 106) || [8, 9, 37, 39].includes(key) || (key >= 48 && key <= 57))) {
    event.preventDefault()
    event.stopImmediatePropagation()
  }
}

const submitOrder = async () => {
  let response: AxiosResponse
  const paymentId = ref(0)
  paymentId.value = await axios
    .post(
      `http://localhost:8000/payment/?card_type=${cardType.value}&card_number=${cardNumber.value}&expiration_month=${expirationMonth.value}&expiration_year=${expirationYear.value}&security_code=${securityCode.value}`
    )
    .then((res) => res.data)
  console.log(paymentId.value)
  //response = await axios.post(`http://localhost:8000/cart/?cart_id=${route.params.cartId}&payment_id=${paymentId.value}&status=payed`).then((res) => res);
  router.push({ name: 'home' })
}
</script>

<template>
  <div class="payment">
    <h1>Your total is {{ orderPrice }}</h1>
    <h2>Insert your payment information</h2>
    <form>
      <label for="card-type">Card type</label><br />
      <select name="card-type" id="card-type" v-model="cardType">
        <option value="credit">Credit</option>
        <option value="debit">Debit</option></select
      ><br />
      <label for="card-number">Card number</label><br />
      <input
        type="text"
        name="card-number"
        id="card-number"
        v-model="cardNumber"
        @input="formatCardNumber()"
        minlength="19"
        maxlength="19"
        v-on:keydown="(event) => validateDigit(event)"
        placeholder="0000 0000 0000 0000"
      />
      <div class="security-code">
        <label for="security-code">Security code</label><br />
        <input
          type="text"
          name="security-code"
          id="security-code"
          minlength="3"
          maxlength="4"
          v-on:keydown="(event) => validateDigit(event)"
          placeholder="000"
          v-model="securityCode"
        /><br />
      </div>
      <label for="expiration-month">Expiration month</label><br />
      <input
        type="text"
        name="expiration-month"
        id="expiration-month"
        minlength="2"
        maxlength="2"
        v-on:keydown="(event) => validateDigit(event)"
        :placeholder="month"
        v-model="expirationMonth"
      />
      <div class="expiration-year">
        <label for="expiration-year">Expiration year</label><br />
        <input
          type="text"
          name="expiration-year"
          id="expiration-year"
          minlength="4"
          maxlength="4"
          v-on:keydown="(event) => validateDigit(event)"
          :placeholder="year"
          v-model="expirationYear"
        /><br />
      </div>
      <input class="submit-button" type="submit" value="Submit" @click="submitOrder()" />
    </form>
  </div>
  <img src="./payment_view.jpg" class="background-decoration" />
</template>

<style scoped>
h1 {
  margin-top: 0px;
}

h2 {
  margin-top: -10px;
  margin-bottom: 40px;
}

label,
input,
select {
  margin-bottom: 20px;
  margin-right: 5px;
  font-size: 16px;
}

input,
select {
  padding: 10px;
  margin-top: 5px;
  background-color: #eaeaea;
  border: none;
  border-radius: 3px;
}

label {
  font-weight: 600;
}

.security-code,
.expiration-year {
  margin-left: 200px;
  margin-top: -84px;
}

.submit-button {
  background-color: #a7eea2;
  margin-bottom: 0px;
}

.submit-button:hover {
  transition-duration: 0.4s;
  background: linear-gradient(to top, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.15)) #a7eea2;
}

.payment {
  margin: 0px !important;
  position: absolute;
  transform: translateY(25%);
}

.background-decoration {
  background-color: #eaeaea;
  height: 100%;
  width: 60%;
  position: fixed;
  float: right;
  top: 0;
  right: 0;
  object-fit: cover;
  filter: grayscale();
}
</style>
