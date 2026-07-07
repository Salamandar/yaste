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
  console.log(window.location)
  const path = window.location.pathname
  const origin = 'https://paste.yunohost.org' // window.location.origin
  const raw_url = `${origin}/raw${window.location.pathname}`

  const data = path != '/' ? await getData(raw_url) : 'Could not download data'
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
