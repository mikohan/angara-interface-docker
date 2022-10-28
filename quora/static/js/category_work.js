
//##########################################################//
//############### VUE PART STARTS HERE #####################//
//##########################################################//
Vue.use(VueToast);
Vue.component('vue-multiselect', window.VueMultiselect.default);
const vsel = Vue.component('v-select', VueSelect.VueSelect);
let il = {

    template: `<div class="product-main-thumbs">
                <h3>{{ message }}</h3>
                <img style="height: 100px; width: 100px;"
                v-for="prod_img in productImages" :src="prod_img.image" alt="...">
                </div>`,
    // data: function (){
    //     return{
    //         productImages: []
    //     }
    // },
    // methods: {
    //     async getImage(id) {
    //         endpoint = `${ApplicationMainHost}/api/product/images/?product_id=${id}`;
    //         let response = await apiService(endpoint);
    //         this.productImages = response.results;

    //     }
    // }


};

const app = new Vue({
    delimiters: ['{', '}'],
    el: '#app',
    data: {

    },
    created() {

    }
});
