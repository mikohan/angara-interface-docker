<template>
    <div class="container">
        <div class="row">
            <div class="col-4">
                <div :key="brand.id" v-for="brand in test">
                    <a :href="brand.url">{{ brand.name }}</a>
                </div>
                
            </div>
            <div class="col-8">
                <div
                    v-if="isDuplicate !== false"
                    class="alert alert-danger"
                    role="alert"
                >Такой Бренд уже есть</div>
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th scope="col">#</th>
                            <th scope="col">Supp Brand</th>
                            <th scope="col">Ang Brand</th>
                            <th scope="col">Ang Brand</th>
                            <th scope="col">Ang Brand</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr :key="i" v-for="(brand_sup, i) in sup_data">
                            <th scope="row">{{ i + 1 }}</th>
                            <td>{{ brand_sup.ang_brand}}</td>
                            <td>
                                <input
                                    type="text"
                                    class="form-control input-sm"
                                    :class="{ 'bred' : isDuplicate === i }"
                                    @blur="checkDuplicates(insert_brand[i], i)"
                                    v-model="insert_brand[i]"
                                    placeholder="Введите название бренда"
                                />
                            </td>
                            <td>{{ insert_brand[i] | upper }}</td>
                            <td>
                                <span
                                    v-if="insert_brand[i]"
                                    class="badge badge-pill badge-success"
                                >Сохранено!</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>


<script>
import { apiService } from "@/common/api.service";
export default {
    data() {
        return {
            test: [],
            sup_data: [],
            insert_brand: [],
            isDuplicate: false
        };
    },
    methods: {
        get_request() {
            let endpoint = "/lang/paradigms/";
            apiService(endpoint).then(data => {
                this.test.push(...data.results);
            });
            /* eslint-disable no-console */
            //console.log(this.test);
        },
        async post_request() {
            let endpoint = '';
            let data = {
                
            }
            const response = await apiService(endpoint, "POST", data);
            console.log(response);
        },
        getSupplierBrands(id) {
            let endpoint = `/api/brands/brand_sup_not_exists/${id}/`;
            apiService(endpoint).then(data => {
                this.sup_data.push(...data.results);
            });
        },
        async checkDuplicates(brand = "not_existing_brand", i) {
            if (this.insert_brand[i]) {
                try {
                    let endpoint = `api/brands/check_duplicates/${brand}/`;
                    const data = await apiService(endpoint);

                    if (data.brand !== "") {
                        this.isDuplicate = i;
                    } else {
                        this.isDuplicate = false;
                        this.sendDataToServer(i);
                    }
                } catch (e) {
                    console.log(e);
                }
            }
        },
        async sendDataToServer(i) {
            let endpoint = "/api/brands/list/";
            try {
                const response = await apiService(endpoint, "POST", {
                    brand: this.insert_brand[i]
                });
                console.log(response);
            } catch (e) {
                alert("Can't send data to server!");
            }
        }
    },
    created() {
        this.get_request();
        this.getSupplierBrands(1);
    }
};
</script>

<style scoped>
.bred {
    background-color: #f8d7da;
}
</style>