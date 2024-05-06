import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'

import App from './App.vue'
import MainView from './views/MainView.vue'
import PaymentView from './views/PaymentView.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: "/",
         name: "home",
         component: MainView
        },
        {name: "payment",
         path: "/payment/:cartId",
         component: PaymentView
        }

    ]
});

const app = createApp(App).use(createPinia()).use(router).mount('#app');

