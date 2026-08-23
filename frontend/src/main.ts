import './assets/main.css'

import 'highlight.js/styles/stackoverflow-light.css'
import hljs from 'highlight.js/lib/common';
import hljsVuePlugin from '@highlightjs/vue-plugin'

import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)
app.use(hljsVuePlugin)
app.mount('#app')
