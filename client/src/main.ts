import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import Lara from '@primevue/themes/lara'
import { definePreset } from '@primevue/themes'


const MyPreset = definePreset(Lara, {
    semantic: {
        primary: {
            50:  '{gray.50}',
            100: '{gray.100}',
            200: '{gray.200}',
            300: '{gray.300}',
            400: '{gray.400}',
            500: '{gray.500}',
            600: '{gray.600}',
            700: '{gray.700}',
            800: '{gray.800}',
            900: '{gray.900}',
            950: '{gray.950}'
        }
    }
});

const primeVueOpts = { theme: { preset: MyPreset }}

const pinia = createPinia()
createApp(App)
    .use(router)
    .use(pinia)
    .use(PrimeVue, primeVueOpts)
    .mount('#app')
