export function getRawPasteUrl(): [string | null, string | null] {
  const base = import.meta.env.BASE_URL

  let pasteServer = ''
  let pasteId = ''
  if (window.location.href.startsWith(base)) {
    pasteServer = base
    pasteId = window.location.href.slice(base.length)
  } else if (window.location.pathname.startsWith(base)) {
    pasteServer = `${window.location.origin}${base}`
    pasteId = window.location.pathname.slice(base.length)
  }

  const envPasteServer = import.meta.env.VITE_API_SERVER
  if (envPasteServer !== undefined && envPasteServer !== '') {
    pasteServer = envPasteServer
  }

  // Here this can be customized for split runtime
  // pasteServer = 'https://paste.yunohost.org'

  // Sanitize url
  if (pasteId == '' || pasteId == '/') {
    return [null, null]
  }
  const extension = pasteId.includes('.') ? pasteId.split('.').pop() || '' : ''
  pasteId = pasteId.replace(/\.[^/.]+$/, '')
  console.log(pasteId, extension)

  const raw_url = `${pasteServer}/raw/${pasteId}`.replace(/([^:]\/)\/+/g, '$1')
  return [raw_url, extension]
}

export async function getRawData(url: string): Promise<string | null> {
  return fetch(url).then(
    async (response) => {
      if (!response.ok) {
        return null
      }
      return response.text().then(
        async (data) => {
          return data
        },
        async () => {
          return null
        },
      )
    },
    async () => {
      return null
    },
  )
}
