<template>
    <div class="container">
        <div class="row">
            <div class="col-12 text-center">
                <h4>
                    Поставщиков:
                    <span class="badge badge-secondary">{{ suppliers_count }}</span>
                </h4>
            </div>
        </div>
        <div class="row">
            <div class="col-6">
                <table class="table table-sm table-hover">
                    <thead>
                        <tr>
                            <th scope="col">#</th>
                            <th scope="col">First</th>
                            <th scope="col">Last</th>
                            <th scope="col">Handle</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr :key="supplier.id" v-for="supplier in suppliers">
                            <th scope="row">{{ supplier.id }}</th>
                            <td><router-link :to="{ name: 'supplier', params: {pk: supplier.id } }"
                            :passedPk="supplier.id"
                            >{{ supplier.name }}</router-link></td>
                            <td>{{ supplier.weight }}</td>
                            <td>@mdo</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
/* eslint-disable no-console */
import { apiService } from "@/common/api.service";
export default {
    data() {
        return {
            suppliers: [],
            suppliers_count: 0
        };
    },
    methods: {
        async getSuppliers() {
            let endpoint = "/api/brands/supplires/";
            const data = await apiService(endpoint);
            if (data.results != undefined) {
                this.suppliers = data.results;
            } else {
                this.suppliers = data;
            }
            this.suppliers_count = data.count;
        }
    },
    created() {
        this.getSuppliers();
    }
};
</script>