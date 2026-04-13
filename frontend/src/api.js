const base = import.meta.env.BASE_URL.replace(/\/$/, '')

export function api(path) {
  return `${base}${path}`
}
