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
      <i>
        <slot name="cart-icon"></slot>
      </i>
    </div>
  </template>

<style scoped>
.image {
  background-color: #333;
  width: 300px;
  height: 300px;
}
</style>