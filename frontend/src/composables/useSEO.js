export function useSEO({ title, description }) {
  const baseTitle = 'Auto Profiling'

  function update(pageTitle, pageDescription) {
    document.title = pageTitle ? `${pageTitle} | ${baseTitle}` : baseTitle

    let meta = document.querySelector('meta[name="description"]')
    if (!meta) {
      meta = document.createElement('meta')
      meta.name = 'description'
      document.head.appendChild(meta)
    }
    meta.content = pageDescription || 'Plataforma interactiva de Data Profiling'
  }

  if (title || description) {
    update(title, description)
  }

  return { update }
}
