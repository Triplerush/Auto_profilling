<script setup>
defineProps({
  data: { type: Object, required: true },
})
</script>

<template>
  <div class="card">
    <h2 class="section-title first">Resumen de Salud</h2>
    <div class="results-grid">
      <div class="metric">
        <div class="value">{{ data.health_summary.total_rows.toLocaleString() }}</div>
        <div class="label">Filas</div>
      </div>
      <div class="metric">
        <div class="value">{{ data.health_summary.total_columns }}</div>
        <div class="label">Columnas</div>
      </div>
      <div class="metric">
        <div class="value">{{ data.health_summary.memory_usage_mb }} MB</div>
        <div class="label">Memoria RAM</div>
      </div>
      <div class="metric">
        <div class="value">{{ data.health_summary.duplicate_percent }}%</div>
        <div class="label">Duplicados</div>
      </div>
      <div class="metric">
        <div class="value">{{ data.health_summary.total_null_percent }}%</div>
        <div class="label">Nulos Totales</div>
      </div>
    </div>

    <h2 class="section-title">Limpieza Aplicada</h2>
    <div class="results-grid">
      <div class="metric">
        <div class="value">{{ data.cleaning_summary.strings_normalized }}</div>
        <div class="label">Cadenas normalizadas</div>
      </div>
      <div class="metric">
        <div class="value">
          {{ data.cleaning_summary.empty_rows_removed }} / {{ data.cleaning_summary.empty_cols_removed }}
        </div>
        <div class="label">Filas / Cols vacias</div>
      </div>
      <div class="metric">
        <div class="value">{{ data.cleaning_summary.duplicates_removed }}</div>
        <div class="label">Duplicados eliminados</div>
      </div>
      <div class="metric">
        <div class="value">{{ data.cleaning_summary.values_coerced }}</div>
        <div class="label">Valores coercionados</div>
      </div>
      <div class="metric">
        <div class="value">{{ data.cleaning_summary.outliers_flagged }}</div>
        <div class="label">Atipicos marcados</div>
      </div>
      <div class="metric">
        <div class="value">{{ data.cleaning_summary.dlq_records }}</div>
        <div class="label">Registros DLQ</div>
      </div>
    </div>

    <h2 class="section-title">Detalle por Columna</h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Columna</th>
            <th>Tipo</th>
            <th>Nulos</th>
            <th>% Nulos</th>
            <th>Unicos</th>
            <th>% Unicos</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="col in data.health_summary.columns" :key="col.name">
            <td>{{ col.name }}</td>
            <td>{{ col.dtype }}</td>
            <td>{{ col.null_count }}</td>
            <td>{{ col.null_percent }}%</td>
            <td>{{ col.unique_count }}</td>
            <td>{{ col.unique_percent }}%</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="download-section">
      <a class="btn-outline" :href="data.download_url">Descargar CSV limpio</a>
      <a
        v-if="data.cleaning_summary.dlq_records > 0"
        class="btn-outline"
        :href="data.download_url + '/dlq'"
      >
        Descargar DLQ
      </a>
    </div>
  </div>
</template>

<style scoped>
.card {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 1.5rem;
}
.section-title {
  font-size: 1rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-top: 1.25rem;
  margin-bottom: 0.5rem;
}
.section-title.first { margin-top: 0; }
.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}
.metric {
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
}
.metric .value { font-size: 1.5rem; font-weight: 700; color: #38bdf8; }
.metric .label { font-size: 0.75rem; color: #94a3b8; margin-top: 0.25rem; }
.table-wrap { overflow-x: auto; }
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0.5rem;
  font-size: 0.8rem;
}
th, td {
  padding: 0.5rem 0.75rem;
  text-align: left;
  border-bottom: 1px solid #334155;
}
th { color: #94a3b8; font-weight: 500; }
td { color: #e2e8f0; }
.download-section {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}
.btn-outline {
  padding: 0.5rem 1rem;
  background: transparent;
  color: #38bdf8;
  border: 1px solid #38bdf8;
  border-radius: 8px;
  font-size: 0.85rem;
  cursor: pointer;
  text-decoration: none;
  transition: background 0.2s;
}
.btn-outline:hover { background: rgba(56, 189, 248, 0.1); }
</style>
