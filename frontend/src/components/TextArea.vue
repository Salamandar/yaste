<script setup lang="ts">
import { ref, onMounted } from 'vue'
import '../assets/solarized_dark.css'
import hljs from 'highlight.js/lib/core'
import { getRawPasteUrl, getRawData, pushRawData } from './api'

const pasteData = ref({ code: '', linenos: '', editable: false })
const textValue = ref('')

async function setData(data: string, language: string) {
  if (data.slice(-1) != '\n') {
    data = data + '\n'
  }

  language = hljs.getLanguage(language) == undefined ? 'plaintext' : language
  const highlighted = hljs.highlight(data, { language: language })
  // const highlighted = hljs.highlightAuto(data);

  const linecount = data.split('\n').length
  let linenos = ''
  for (let i = 1; i < linecount + 1; i++) {
    linenos += `${i}<br/>`
  }
  pasteData.value = {
    code: highlighted.value,
    linenos: linenos,
    editable: false,
  }
}

async function setEditable() {
  pasteData.value = {
    code: '',
    linenos: '>',
    editable: true,
  }
}
async function savePaste() {
  if (textValue.value == '') {
    return
  }
  // Try to detect the file type...
  let ext = ''
  const highlighted = hljs.highlightAuto(textValue.value)
  if (highlighted.language != null) {
    const lang = hljs.getLanguage(highlighted.language)?.aliases?.at(0)
    ext = `.${lang}`
  }
  const pasteUrl = await pushRawData(textValue.value)
  if (pasteUrl != null) {
    console.log(pasteUrl)
    window.location.href = pasteUrl + ext
  }
}

onMounted(async () => {
  const [rawPasteUrl, extension] = getRawPasteUrl()
  if (rawPasteUrl == null) {
    return await setEditable()
  }
  const data = await getRawData(rawPasteUrl)
  if (data == null) {
    await setData('Could not download paste', 'plaintext')
    return
  }
  await setData(data, extension || 'plaintext')
})
</script>

<template>
  <div class="codezone" ref="codezone">
    <div class="linenos hljs-comment" v-html="pasteData.linenos" />
    <pre class="hljs" v-html="pasteData.code" v-if="!pasteData.editable" />
    <textarea
      class="hljs"
      spellcheck="false"
      placeholder="Paste your data here and ctrl-s"
      v-model="textValue"
      v-if="pasteData.editable"
      @keydown.ctrl.s.prevent="savePaste"
    />
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

.codezone textarea {
  font-size: 13px;
  border: none;
  outline: none;
}
</style>
