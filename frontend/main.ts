import { createApp } from 'vue'
import '@/styles.css'
import widgets from '@/widgets'

function mountWidgets() {
  document.querySelectorAll('[data-vue-widget]').forEach((el) => {
    const widgetName = el.getAttribute('data-vue-widget')
    if (widgetName && widgetName in widgets) {
      const app = createApp(widgets[widgetName as keyof typeof widgets])
      app.mount(el)
    }
  })
}

mountWidgets()
