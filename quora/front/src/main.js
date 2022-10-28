import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import '@fortawesome/fontawesome-free/css/all.css'
import '@fortawesome/fontawesome-free/js/all.js'

Vue.config.productionTip = false
Vue.filter('upper', (value) => {
  if (!value) {
    return ''
  }
  value = value.toString();
  return value.toUpperCase();
});

Vue.filter('capitalize', (value) => {
  if (!value) return ''
  value = value.toString()
  return value.charAt(0).toUpperCase() + value.slice(1)
});

Vue.filter('trim_text', value => {
  return value.trim();
});


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
