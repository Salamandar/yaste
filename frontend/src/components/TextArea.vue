<script setup lang="ts">
import { ref, onMounted } from 'vue'
import '../assets/solarized_dark.css'
import hljs from 'highlight.js/lib/core'
import { getRawPasteUrl, getRawData } from './api'

const pasteData = ref({ code: '', linenos: '' })

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
  const rawPasteUrl = getRawPasteUrl()
  if (rawPasteUrl) {
    const data = await getRawData(rawPasteUrl)
    await setData(data)
  } else {
    await setData('No paste requested')
  }
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

.hljs {
  flex-basis: 100%;
}
</style>
