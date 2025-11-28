import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  define: {
    // Excalidraw requires process.env.IS_PREACT to be defined in some versions
    "process.env.IS_PREACT": JSON.stringify("false"),
  },
})