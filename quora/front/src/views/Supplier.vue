<template>
    <div>
        <div class="container">
            <div class="row mt-2">
                <div class="col-12"></div>
                <ul class="list-inline top-list">
                    <li class="list-inline-item american-river">{{ supplierName }}</li>
                    <li class="list-inline-item chi-gong">Осталось: {{ brandsCount }}</li>
                </ul>
            </div>
            <div class="row mt-2">
                <div class="col-4">
                    <!-- Only show if loading is true -->
                    <div class="d-flex justify-content-center">
                    <div v-if="loading" v-cloak class="spinner-border text-success mt-3 mb-3" style="width: 3rem; height: 3rem;" role="status">
                        <span class="sr-only">Loading...</span>
                    </div>
                    </div>
                    <table v-if="!loading" class="table table-hover table-sm">
                        <thead>
                            <tr>
                                <th style="width: 20%" scope="col">#</th>
                                <th style="width: 70%" scope="col">Бренд</th>
                                <th style="width: 10%" scope="col">Частотность</th>
                                <th>
                                    <div class="custom-control custom-checkbox">
                                        <input
                                            type="checkbox"
                                            class="custom-control-input"
                                            id="head"
                                        />
                                        <label class="custom-control-label" for="head"></label>
                                    </div>
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr :key="i" v-for="(brand, i) in supplier">
                                <th scope="row">{{ i }}</th>
                                <td
                                    @click="sendBrandToInput(brand.ang_brand, i)"
                                    class="dup-brand"
                                >{{ brand.ang_brand | trim }}</td>
                                <td>{{ brand.count }}</td>
                                <td>
                                    <div class="custom-control custom-checkbox">
                                        <input
                                            :value="{'ang_brand': brand.ang_brand}"
                                            v-model.trim="nbnList"
                                            type="checkbox"
                                            class="custom-control-input"
                                            :id="i"
                                        />
                                        <label class="custom-control-label" :for="i"></label>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="col-4">
                    <div class="row">
                        <div class="col-12">
                            <form @submit.prevent="sendBrand">
                                <div class="input-group input-group-sm mb-3">
                                    <input
                                        @blur="checkDuplicates(myForm.brand)"
                                        type="text"
                                        class="form-control"
                                        aria-label="Small"
                                        aria-describedby="inputGroup-sizing-sm"
                                        v-model.trim="myForm.brand"
                                    />
                                </div>
                                <div
                                    :key="key"
                                    v-for="(row, key) in rows"
                                    class="input-group input-group-sm mb-3"
                                >
                                    <input
                                        ref="myid"
                                        class="form-control"
                                        type="text"
                                        v-model.trim="myForm.brand_supplier[key]"
                                    />
                                </div>
                                <div>
                                    <button
                                        class="btn btn-outline-primary btn-sm"
                                        type="submit"
                                    >Сохранить</button>
                                    <button
                                        @click.prevent="addRow"
                                        class="btn btn-outline-primary btn-sm ml-1 float-right"
                                    >+</button>
                                </div>
                            </form>
                        </div>
                    </div>
                    <div v-if="nbnList.length != 0" class="row mt-4">
                        <div class="col-12">
                            <div class="table-responsive">
                                <table class="table">
                                    <thead>
                                        <tr>
                                            <th scope="col">Выбрано для NBN</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr :key="j" v-for="(val, j) in nbnList">
                                            <td class="prunus-avium bold-500">{{ val.ang_brand }}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <button
                                @click="updateNbn"
                                class="btn btn-outline-warning btn-sm"
                            >Сохранить</button>
                        </div>
                    </div>
                </div>
                <div class="col-4">
                    <div
                        v-if="brandExists"
                        class="alert alert-warning alert-pink"
                        role="alert"
                    >Бренд {{ }} Уже Есть! Редактировать.</div>

                    <div v-if="listDuplicates.length != 0" class="row mt-4">
                        <div class="col-12">
                            <table class="table table-sm">
                                <thead>
                                    <tr>
                                        <th style="width: 30%" scope="col">#</th>
                                        <th style="width: 60%" scope="col">Бренд</th>
                                        <th style="width: 30%" scope="col">Удалить</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr :key="dup.id" v-for="dup in listDuplicates">
                                        <th scope="row">{{ dup.id }}</th>
                                        <td
                                            class="dup-brand"
                                            @click="checkDuplicates2(dup.id)"
                                        >{{ dup.brand | upper }}</td>
                                        <td
                                            class="red-trash"
                                            @click="deleteWholeBrand(dup.id, dup.brand)"
                                        >
                                            <i class="far fa-trash-alt"></i>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <div class="list-group"></div>
                    <div v-if="brandExists" class="row mt-4">
                        <div class="col-12">
                            <div>
                                <form @submit.prevent="updateExistingBrand">
                                    <div class="input-group input-group-sm mb-3">
                                        <input v-model.trim="existFormData.brand" class="form-control" />
                                    </div>
                                    <div
                                        :key="val.pk"
                                        v-for="(val) in existFormData.brand_supplier"
                                        class="input-group input-group-sm mb-3"
                                    >
                                        <input v-model.trim="val.ang_brand" class="form-control" />
                                        <span
                                            @click="deleteBrandRow(val.pk)"
                                            class="input-group-addon"
                                        >
                                            <i class="far fa-trash-alt"></i>
                                        </span>
                                    </div>
                                    <button
                                        type="submit"
                                        class="btn btn-outline-primary btn-sm float-left"
                                    >Сохранить</button>
                                    <button
                                        @click.prevent="addEmptyRow"
                                        class="btn btn-outline-primary btn-sm ml-1 float-right"
                                    >+</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row mb-5 mt-2">
                <div class="col-12">
                    <nav aria-label="Page navigation example">
                        <ul class="pagination">
                            <li class="page-item" :class="{active: previous, disabled: !previous}">
                                <a
                                    @click.prevent="getSupplier(pk)"
                                    class="page-link"
                                    href="#"
                                >Previous</a>
                            </li>
                            <li class="page-item">
                                <a class="page-link" href="#">1</a>
                            </li>
                            <li class="page-item">
                                <a class="page-link" href="#">2</a>
                            </li>
                            <li class="page-item">
                                <a class="page-link" href="#">3</a>
                            </li>
                            <li class="page-item" :class="{active: next, disabled: !next}">
                                <a @click.prevent="getSupplier(pk)" class="page-link" href="#">Next</a>
                            </li>
                        </ul>
                    </nav>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
/* eslint-disable no-console */
import { apiService } from "@/common/api.service";
export default {
    props: ["pk"],
    data() {
        return {
            loading: false,
            save_result: {},
            supplier: {},
            brandsCount: 0,
            supplierName: null,
            test: null,
            myForm: {
                brand: null,
                brand_supplier: [],
                check: null
            },
            rows: [
                {
                    ang_brand: ""
                }
            ],
            existFormData: {},
            brandExists: false,
            listDuplicates: [],
            nbnList: [],
            next: null,
            previous: null
        };
    },

    computed: {},
    methods: {
        // Checking brands to sent to nbn

        // Making different forms for brand name if it contains more than one word

        makeBrandDifferentForms(brand) {
            var resName;
            brand = brand.trim().toLowerCase();
            if (brand.includes("-")) {
                let arr = brand.split("-");
                resName = arr.join(" ");
            } else if (brand.includes(" ")) {
                let arr = brand.split(" ");
                resName = arr.join("-");
            } else {
                resName = null;
            }
            return resName;
        },
        removeDash(brand) {
            var resName;
            brand = brand.trim().toLowerCase();
            if (brand.includes("-")) {
                let arr = brand.split("-");
                resName = arr.join(" ");
            } else {
                resName = brand;
            }
            return resName;
        },

        //Adding row dinamically to page on click(probably need add key listener)

        addRow: function() {
            this.rows.push({
                brand_supplier: ""
            });
        },

        //Getting list of suppliers from server
        //######################################// "http://localhost:8000/api/brands/brand_sup_not_exists/82/?page=2"

        async getSupplier(pk) {
            
            let endpoint = `/api/brands/brand_sup_not_exists/${pk}/`;
            if (this.next) {
                endpoint = this.next;
            }
            if (this.previous) {
                endpoint = this.previous;
            }
            
            this.loading = true;
            const data = await apiService(endpoint);
            this.loading = false;
            
            if (data.next != null) {
                this.next = data.next;
            } else {
                this.next = null;
            }
            if (data.previous != null) {
                this.previous = data.previous;
            } else {
                this.previous = null;
            }
            

            this.supplier = data.results;
            this.brandsCount = data.count;
            this.supplierName = data.supplier;
            
        },

        //Filling input with brand form left side of table

        sendBrandToInput(title) {
            title = title.toLowerCase();
            this.myForm.brand = this.removeDash(title);
            this.myForm.brand_supplier[0] = title.toLowerCase();

            let chttl = this.makeBrandDifferentForms(title);
            if (chttl) {
                this.rows.push(title);
                this.myForm.brand_supplier[1] = chttl;
            } else {
                this.myForm.brand_supplier.forEach((el, i) => {
                    if (i > 0) {
                        this.myForm.brand_supplier[i] = null;
                    }
                });
                this.rows.forEach((el, i) => {
                    if (i > 0) {
                        this.rows.splice(i, 2);
                    }
                });
            }
            this.rows.filter(el => {
                return el != null;
            });
        },

        // Checking Duplicates for brand if not - create, if yes - update

        checkDuplicates(brand = "not_existing_brand") {
            try {
                let endpoint = `/api/brands/check_duplicates/${brand}/`;
                const data = apiService(endpoint);
                return data;
            } catch (e) {
                console.log(e);
            }
        },

        // List duplicates to make a choise

        // Working with single brand duplicated edit precisely

        async checkDuplicates2(pk) {
            try {
                let endpoint = `/api/brands/brand_dup_detail/${pk}/`;
                const data = await apiService(endpoint);
                if (data.id !== undefined) {
                    this.existFormData = await this.manageExisting(data.id);
                    await this.addEmptyRow();
                } else {
                    this.existFormData = {};
                }
            } catch (e) {
                console.log(e);
            }
        },

        //Adding row to update form

        addEmptyRow() {
            if (
                this.existFormData !== undefined &&
                this.existFormData.brand_supplier[-1] !== ""
            ) {
                this.existFormData.brand_supplier.push({ ang_brand: "" });
            }
        },

        // Deleting whole brand

        async deleteWholeBrand(pk, brand) {
            let endpoint = `/api/brands/brand_update/list/${pk}/`;
            await apiService(endpoint, "DELETE");
            await this.checkDuplicates(brand);
            await this.getSupplier(this.pk);
            this.previous = null;
            this.brandExists = false;
            this.listDuplicates = [];
        },

        // Deleting brand row from array

        deleteBrandRow(key) {
            const result = this.existFormData.brand_supplier.findIndex(name => {
                return name.pk == key;
            });
            //const index = this.existFormData.brand_supplier.indexOff(result);
            this.existFormData.brand_supplier.splice(result, 1);
        },

        //Save data to server

        async sendBrand() {
            let chkDup = await this.checkDuplicates(this.myForm.brand);

            this.listDuplicates = chkDup;

            if (chkDup.length == 0) {
                let arr = [];
                this.myForm.brand_supplier.forEach(element => {
                    arr.push({ ang_brand: element });
                });
                this.myForm.brand_supplier = arr;
                const endpoint = "/api/brands/new_brands/";
                const res = await apiService(endpoint, "POST", this.myForm);
                this.save_result = res;
                this.previous = null;
                this.next = null;
                this.getSupplier(this.pk);
                this.myForm.brand = null;
                this.myForm.brand_supplier = [];
                this.rows = [
                    {
                        ang_brand: ""
                    }
                ];
            } else {
                //this.checkDuplicates2(chkDup.brand);
                this.brandExists = true;
            }
        },
        // Updating No Brand Name item only

        async updateNbn() {
            const nbnPk = 847;
            let endpoint = `/api/brands/brand_update/list/${nbnPk}/`;
            const nbn = await apiService(endpoint, "GET");
            nbn.brand_supplier.push(...this.nbnList);

            const res = await apiService(endpoint, "PUT", nbn);
            this.save_result = res;
            if (res) {
                this.previous = null;
                this.getSupplier(this.pk);
                this.nbnList = [];
            }
        },

        // Sending existing brand updated data

        async updateExistingBrand() {
            let arr = [];
            this.existFormData.brand_supplier.forEach(element => {
                arr.push(element);
            });
            this.existFormData.brand_supplier = arr;
            const pk = this.existFormData.id;
            let endpoint = `/api/brands/brand_update/list/${pk}/`;

            const last_index = this.existFormData.brand_supplier.length - 1;
            if (this.existFormData.brand_supplier[last_index] !== undefined) {
                if (
                    this.existFormData.brand_supplier[last_index].ang_brand ==
                    ""
                ) {
                    this.existFormData.brand_supplier.splice(-1, 1);
                }
            }

            const res = await apiService(endpoint, "PUT", this.existFormData);
            this.save_result = res;
            this.existFormData = {};
            this.brandExists = false;
            //await this.checkDuplicates(brand);
            this.previous = null;
            this.next = null;
            await this.getSupplier(this.pk);
            this.listDuplicates = [];
            //this.myForm = {};
        },

        // If brand exists add form to manage existing brand

        async manageExisting(pk) {
            let endpoint = `/api/brands/brand_update/list/${pk}/`;
            const data = apiService(endpoint);
            this.brandExists = true;
            return data;
        }
    },
    created() {
        this.getSupplier(this.pk);
    }
};
</script>

<style scoped>
.input-group-addon {
    color: #e84393;
    font-size: 1rem;
    padding-left: 0.3rem;
}
.red-trash {
    color: #e84393;
    cursor: pointer;
}
.dup-brand {
    color: #007bff;
    font-weight: bold;
    cursor: pointer;
}
.alert-pink {
    color: #e84393;
    background-color: #fd79a833;
    border-color: #e8439333;
}
.custom-control-label::before,
.custom-control-label::after {
    width: 1rem;
    height: 1rem;
}

.top-list {
    font-weight: bold;
}
.top-list li {
    margin-right: 20px;
}
.american-river {
    color: #636e72;
}
.mint-leaf {
    color: #00b894;
}
.robbins-egg {
    color: #00cec9;
}
.chi-gong {
    color: #d63031;
}
.pointer {
    cursor: pointer;
}
.prunus-avium {
    color: #e84393;
}
.bold-500 {
    font-weight: 500;
}
</style>

