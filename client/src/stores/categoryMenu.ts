import { ref } from 'vue'
import { defineStore } from 'pinia'


export function createCategoryMenuStore(categoriesList: Record<string, boolean>){
  return defineStore('categoryMenu', () => {
  const categoryMenuState = ref<Record<string, boolean>>(categoriesList);

  return { categoryMenuState }
})
}