import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
//import Brands from '../views/Brands.vue'
import Suppliers from '../views/Suppliers.vue'
import Supplier from '../views/Supplier.vue'

Vue.use(VueRouter)

const routes = [
  
  {
    path: '/vuehome',
    name: 'home',
    component: Home
  },
  // {
  //   path: '/brands/',
  //   name: 'brands',
  //   component: Brands
  // },
  {
    path: '/suppliers',
    name: 'suppliers',
    component: Suppliers
  },
  {
    path: '/supplier/:pk/',
    name: 'supplier',
    component: Supplier,
    props: true
  },
  {
    path: '*',
    name: 'page-not-foud',
    component: Home
  }
  // {
  //   path: '/about',
  //   name: 'about',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  // }
]


const router = new VueRouter({
  mode: 'history',
  //base: process.env.BASE_URL,
  base: '/interface/',
  routes
})

export default router
