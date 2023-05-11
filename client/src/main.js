import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'
import { IonicVue } from '@ionic/vue';
import '@ionic/core/css/ionic.bundle.css';

const app = createApp(App)
.use(IonicVue)
app.mount('#app');