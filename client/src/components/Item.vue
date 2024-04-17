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
        <img class="cart-icon" src="./images/add-cart.png"/>
    </div>
  </template>

<style scoped>

:slotted(img) {
  width: 210px;
  height: 180px;
  border-radius: 10px;
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
  box-shadow: 5px;
}
</style>