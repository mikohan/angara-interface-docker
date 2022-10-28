


let vi = new Vue({
    delimiters: ['{', '}'],
    el: '#app-list',
    filters: {
        capitalize: function (value) {
            if (!value) return ''
            value = value.toString()
            return value.charAt(0).toUpperCase() + value.slice(1)
        }
    },
    data: {
        modelsList: [],
        chekBoxList: [],
        checkedArray: [],
        alphabet: [{ 'name': 'а', 'selected': false }
            , { 'name': 'б', 'selected': false }
            , { 'name': 'в', 'selected': false }
            , { 'name': 'г', 'selected': false }
            , { 'name': 'д', 'selected': false }
            , { 'name': 'е', 'selected': false }
            , { 'name': 'ж', 'selected': false }
            , { 'name': 'з', 'selected': false }
            , { 'name': 'и', 'selected': false }
            , { 'name': 'й', 'selected': false }
            , { 'name': 'к', 'selected': false }
            , { 'name': 'л', 'selected': false }
            , { 'name': 'м', 'selected': false }
            , { 'name': 'н', 'selected': false }
            , { 'name': 'о', 'selected': false }
            , { 'name': 'п', 'selected': false }
            , { 'name': 'р', 'selected': false }
            , { 'name': 'с', 'selected': false }
            , { 'name': 'т', 'selected': false }
            , { 'name': 'у', 'selected': false }
            , { 'name': 'ф', 'selected': false }
            , { 'name': 'х', 'selected': false }
            , { 'name': 'ц', 'selected': false }
            , { 'name': 'ч', 'selected': false }
            , { 'name': 'ш', 'selected': false }
            , { 'name': 'щ', 'selected': false }
            , { 'name': 'э', 'selected': false }
            , { 'name': 'ю', 'selected': false }
            , { 'name': 'я', 'selected': false }
        ],
        search: 65,
    },
    methods: { //Method will update product inline on product list page
        async deleteProduct(id) {
            const endpoint = `${ApplicationMainHost}/api/product/detail/${id}/`;
            let result = await apiService(endpoint, 'DELETE');
            location.reload();
        },
        check(e) {
            if (e.target.checked) {
                this.checkedArray.push(e.target.value);
            } else {
                const index = this.checkedArray.indexOf(e.target.value);
                this.checkedArray.splice(index, 1);
            }
            localStorage.setItem('letters', JSON.stringify(this.alphabet));
        },
        submit: function () {
            localStorage.removeItem('letters');
            localStorage.setItem('letters', JSON.stringify(this.alphabet));
        },
        getLetters() {
            if (localStorage.getItem('letters')) {
                this.alphabet = JSON.parse(localStorage.getItem('letters'));
            }
        }
    },
    created() {
        this.getLetters();
    }
});


