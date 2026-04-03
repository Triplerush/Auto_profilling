<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <header>
    <div class="header-inner" @click="router.push('/')">
      <h1 class="logo">Auto Profiling</h1>
      <p class="subtitle">Plataforma Interactiva de Data Profiling</p>
    </div>
  </header>
  <main>
    <router-view />
  </main>
</template>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {
  --bg-dark: #0f172a;
  --bg-card: #1e293b;
  --bg-code: #0d1117;
  --border: #334155;
  --accent: #38bdf8;
  --accent-hover: #7dd3fc;
  --text-primary: #e2e8f0;
  --text-secondary: #94a3b8;
  --danger: #ef4444;
  --warning: #f59e0b;
  --success: #22c55e;
  --purple: #a78bfa;
  --green: #34d399;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: var(--bg-dark);
  color: var(--text-primary);
  min-height: 100vh;
}
header {
  width: 100%;
  padding: 1rem 2rem;
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
}
.header-inner { cursor: pointer; user-select: none; }
.logo { font-size: 1.3rem; color: var(--accent); }
.subtitle { font-size: 0.8rem; color: var(--text-secondary); margin-top: 0.15rem; }
main {
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 1.5rem;
}
</style>
