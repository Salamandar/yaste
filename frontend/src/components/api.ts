export function getRawPasteUrl(): string | null {
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
  if (pasteId != '' && pasteId != '/') {
    const raw_url = `${pasteServer}/raw/${pasteId}`.replace(/([^:]\/)\/+/g, '$1')
    return raw_url
  }
  return null
}

export async function getRawData(url: string): Promise<string> {
  const not_found = 'Could not download paste'
  return fetch(url).then(
    async (response) => {
      if (!response.ok) {
        return not_found
      }
      return response.text().then(
        async (data) => {
          return data
        },
        async () => {
          return not_found
        },
      )
    },
    async () => {
      return not_found
    },
  )
}
