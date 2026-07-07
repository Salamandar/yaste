import './assets/main.css'

import 'highlight.js/styles/stackoverflow-light.css'
import hljs from 'highlight.js/lib/core'
import javascript from 'highlight.js/lib/languages/javascript'
import hljsVuePlugin from '@highlightjs/vue-plugin'

import { createApp } from 'vue'
import App from './App.vue'

// let url = "https://paste.yunohost.org/raw/ajoboxeluy";
hljs.registerLanguage('javascript', javascript)
hljs.registerLanguage('yaml', javascript)

const app = createApp(App)
app.use(hljsVuePlugin)
app.mount('#app')
