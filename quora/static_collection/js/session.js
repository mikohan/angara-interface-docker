//Этот код отвечает за загрузку сессии в которой выбираем машину и двигатель
// Так же устанавливаем сессию для работы с новыми товарами
//Возможно использовать при редактировании товаров пока не знаю

//Первый инстанс отвечает за модальное окно и сеттинг сессии
//Второй инстанс отвечает за показ сесси в хедере



var store = {
    debug: false,
    state: {
        selectedSession: 'Select session'
    },
    setSelectedSession(newValue) {
        if (this.debug) console.log('setMessageAction triggered with', newValue)
        this.state.selectedSession = newValue
    }
}
let v = new Vue({
    delimiters: ['{', '}'],
    el: '#modal-default',
    data: {
        car_engine: {},
        car_model: {},
        sharedState: store.state
    },
    methods: {
        async sendSession() {
            send_data = {
                car_model: {
                    id: this.car_model.id,
                },
                car_engine: {
                    id: this.car_engine.id
                }
            }
            store.setSelectedSession(this.car_model.name + ' ' + this.car_engine.name);
            endpoint = `${ApplicationMainHost}/api/product/session/`;
            const data = await apiService(endpoint, 'POST', send_data);
            
        }
    }
});
let showVue = new Vue({
    delimiters: ['{', '}'],
    el: '#show-session',
    data: {
        car_model: {},
        car_engine: {},
        sharedState: store.state
    },
    computed: {
        selectedSession() {
            if (this.car_model) {
                return this.car_model.name + ' ' + this.car_engine.name;
            } else {
                return 'Выбрать параметры';
            }
        }
    },
    methods: {
        async getData() {
            endpoint = `${ApplicationMainHost}/api/product/session/`;
            const data = await apiService(endpoint, 'GET');
            this.car_model = data.car_model;
            this.car_engine = data.car_engine;
            store.setSelectedSession(this.car_model.name + ' ' + this.car_engine.name);
        }
    },
    created() {
        this.getData()
    }
});