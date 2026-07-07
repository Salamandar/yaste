<script setup lang="ts">
import { ref, onMounted } from 'vue'
import '../assets/solarized_dark.css'
import hljs from 'highlight.js/lib/core'

const pasteData = ref({ code: '', linenos: '' })

async function getData(url: string): Promise<string> {
  return fetch(url).then(async (response) => {
    return response.text().then(async (data) => {
      return data
    })
  })
}

async function setData(data: string) {
  if (data.slice(-1) != '\n') {
    data = data + '\n'
  }
  const highlighted = hljs.highlight(data, { language: 'yaml' })
  // const highlighted = hljs.highlightAuto(data);

  const linecount = data.split('\n').length
  let linenos = ''
  for (let i = 1; i < linecount; i++) {
    linenos += `${i}<br/>`
  }
  pasteData.value = {
    code: highlighted.value,
    linenos: linenos,
  }
}

onMounted(async () => {
  const base = import.meta.env.BASE_URL

  let pasteId = ""
  let pasteServer = ""
  if (window.location.href.startsWith(base)) {
    pasteServer = base
    pasteId = window.location.href.slice(base.length)
  } else if (window.location.pathname.startsWith(base)) {
    pasteServer = `${window.location.origin}${base}`
    pasteId = window.location.pathname.slice(base.length)
  }
  console.log(`pasteId = ${pasteId}`)
  // Here this can be customized for split runtime
  // pasteServer = 'https://paste.yunohost.org'

  // Sanitize url
  const raw_url = `${pasteServer}/raw/${pasteId}`.replace(/([^:]\/)\/+/g, "$1");
  const data = pasteId != '' ? await getData(raw_url) : 'No paste requested'
  await setData(data)
})
</script>

<template>
  <div class="codezone" ref="codezone">
    <div class="linenos hljs-comment" v-html="pasteData.linenos" />
    <pre class="hljs" v-html="pasteData.code" />
  </div>
</template>

<style scoped>
.codezone {
  min-width: 100%;
  min-height: 100%;
  font-size: 13px;
  display: flex;
}

.linenos {
  background: #002b36;
  border-right: 1px solid rgba(0, 0, 0, 0.4);
  font-family: monospace;
  text-align: right;

  padding: 0.5em;
  user-select: none;
}
</style>
