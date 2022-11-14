//##########################################################//
//############### VUE PART STARTS HERE #####################//
//##########################################################//
Vue.use(VueToast);
Vue.use(CKEditor);
Vue.component('vue-multiselect', window.VueMultiselect.default);
var ApplicationMainHost = main_host;
console.log(ApplicationMainHost, 'Host from django settings');

const vsel = Vue.component('v-select', VueSelect.VueSelect);
let il = {
  template: `<div class="product-main-thumbs">
                <h3>{{ message }}</h3>
                <img style="height: 100px; width: 100px;"
                v-for="prod_img in productImages" :src="prod_img.image" alt="...">
                </div>`,
};

const app = new Vue({
  delimiters: ['{', '}'],
  el: '#app',
  components: {
    'image-loader': il,
  },
  data: {
    //Crosess
    crossesList: [],
    //Create dual list for related product
    loadRelated: false,
    list1: [{ id: 1, name: 'Запчасть 1', cat_number: '13334h500' }],
    list2: [],
    searchRelated: '',
    chkResponse: [],
    addAtrName: null,
    addAttributeName: false,
    editor: ClassicEditor,
    editorData: '<p>Напишите текст сюда.</p>',
    descriptionId: null,
    addDescriptionButton: false,
    editorConfig: {
      // The configuration of the editor.
    },

    value: [],
    valueEngine: [],
    options: [{ name: 'Vue.js', language: 'JavaScript' }],
    part: {
      car_make_id: null,
      id: null,
      one_c_id: 0,
      name: 'Название Товара',
      name2: 'Доп Параметры',
      cat_number: '',
      oem_number: '',
      category: '',
      brand: 1,
      car_model: {
        name: '',
        carmake: {
          country: {},
        },
      },
      product_cross: [],
      unit: null,
      engine: '',
      active: true,
      engine: {},
    },
    selectCarModelList: [],
    selectUnitList: [],
    selectBrandList: [],
    selectCarEngineList: [],
    selectedUnitId: null,
    selectedBrandId: null,
    selectedCarModelId: null,
    selectedCarEnginelId: null,
    // Image part of code
    productImages: [],
    selectedFiles: [],
    mainImage: 0, // Later needed to implement selected main image by id,
    // Video part of Code
    productVideos: [],
    productVideoUrl: '',
    imageLoading: false,
    attributeFields: [
      {
        id: 0,
        attribute_name: 'attribute',
        attribute_value: 'attr value',
      },
    ],
    attributeList: [],
    main_img: null,
  },
  computed: {
    //search in related product tab
    filteredList() {
      return this.list1.filter((post) => {
        return post.name
          .toLowerCase()
          .includes(this.searchRelated.toLowerCase());
      });
    },
    selectedUnit: {
      get() {
        if (this.selectedUnitId) {
          let s = this.selectedUnitId;
          return s;
        } else {
          let result = this.selectUnitList.filter((a) => {
            return a.id == this.part.unit;
          });
          return result;
        }
      },
      set(val) {
        this.selectedUnitId = val;
      },
    },
    selectedBrand: {
      set(val) {
        this.selectedBrandId = val;
      },
      get() {
        if (this.selectedBrandId) {
          return this.selectedBrandId;
        }
        let result = this.selectBrandList.filter((a) => {
          return a.id == this.part.brand;
        });
        return result;
      },
    },
    selectedCarModel: {
      set(val) {
        this.selectedCarModelId = val;
      },
      get() {
        if (this.selectedCarModelId) {
          return this.selectedCarModelId;
        }
        let result = this.selectCarModelList.filter((a) => {
          return a.id == this.part.car_model.id;
        });
        return result;
      },
    },
    selectedCarEngine: {
      set(val) {
        this.selectedCarEnginelId = val;
      },
      get() {
        if (this.selectedCarEnginelId) {
          return this.selectedCarEnginelId;
        } else if (this.selectCarEngineList) {
          let result = this.selectCarEngineList.filter((a) => {
            return a.id == this.part.engine;
          });
          return result;
        } else {
          return '';
        }
      },
    },
  },

  methods: {
    saveMainImg(id) {
      //send data to server here
      console.log('Imange id ', id, this.part.id);
    },
    //Save all method
    saveAll() {
      try {
        this.saveAttribute();
      } catch (e) {
        console.log('Cannot save attribute! Error ' + e);
      }
      try {
        this.saveDescription();
      } catch (e) {
        console.log('Cannot save description! Error ' + e);
      }
      try {
        this.saveRelated();
      } catch (e) {
        console.log('Cannot save Related! Error ' + e);
      }
      try {
        this.editPart();
      } catch (e) {
        console.log('Cannot save Part! Error ' + e);
      }
    },
    //Methods for crosses
    addCrossRow() {
      this.part.product_cross.push({ id: 0, cross: '' });
    },
    async deleteCross(i) {
      this.part.product_cross.splice(i, 1);
    },

    //Methods for related products
    async getProductList(product_list) {
      this.loadRelated = true;
      const endpoint = `${ApplicationMainHost}/api/product/list/`;
      let response = await apiService(endpoint);
      this.list1 = response;
      this.getRelatedProduct(this.part.id);
      this.loadRelated = false;
    },
    async getRelatedProduct(id) {
      //let id = this.part.id;
      const endpoint = `${ApplicationMainHost}/api/product/related/${id}/`;
      let response = await apiService(endpoint);
      let new_arr = [];
      for (let i = 0; i < response.related.length; i++) {
        const find = this.list1.find((item) => item.id == response.related[i]);
        new_arr.push(find);
      }
      this.list2 = new_arr;
    },
    async saveRelated() {
      let id = this.part.id;
      const endpoint = `${ApplicationMainHost}/api/product/related/${id}/`;
      let related_list = [];
      for (let i = 0; i < this.list2.length; i++) {
        related_list.push(this.list2[i].id);
      }
      const data = {
        product: this.part.id,
        related: related_list,
      };
      let response = await apiService(endpoint, 'PUT', data);
      if (response) {
        this.successToast('Сопутствующие сохранены!');
      } else {
        this.errorToast('Сопутствующие сохранены!');
      }
    },
    oneToRight() {
      let select = document.getElementById('list1').value;
      if (select != '') {
        let i = this.list1.find((e) => e.id == select);
        this.list2.push(i);
        let del = this.list1.indexOf(i);
        this.list1.splice(del, 1);
      }
    },
    oneToLeft() {
      let select = document.getElementById('list2').value;
      if (select != '') {
        let i = this.list2.find((e) => e.id == select);
        this.list1.push(i);
        let del = this.list2.indexOf(i);
        this.list2.splice(del, 1);
      }
    },
    // Attribute portion of code
    async addAttrNameMethod() {
      const endpoint = `${ApplicationMainHost}/api/product/attributes/`;
      const data = {
        name: this.addAtrName,
      };
      let response = await apiService(endpoint, 'POST', data);
      //console.log(response)
      this.attributeList.push({
        attribute_text_name: response.name,
        attribute_value: '',
        id: null,
        product: this.part.id,
        attribute_name: response.id,
      });
      this.addAtrName = null;
      this.addAttributeName = false;
    },
    addAttributeRow() {
      this.attributeFields.push({ id: null, name: '', value: '' });
    },
    async getAttributeList() {
      const endpoint = `${ApplicationMainHost}/api/product/attributes/`;
      let response = await apiService(endpoint);

      this.attributeList = response.results;
    },
    async getAttribute(product_id) {
      const endpoint = `${ApplicationMainHost}/api/product/attribute/?product_id=${product_id}`;
      let response = await apiService(endpoint);
      this.attributeList = response.results;
    },

    // Delete attributes
    async deleteAttribute(id) {
      const endpoint = `${ApplicationMainHost}/api/product/attribute/${id}/`;
      const response = await apiService(endpoint, 'DELETE');
      this.attributeList = this.attributeList.filter((item) => item.id !== id);
    },

    async saveAttribute() {
      /*
            1) implement foreach method in wich get attribute id,
            2) in that loop sending request upon id exists
                If exists: update that attribute
                If not exists: create that attribute
            4) By the way method update is not defined for now
            */
      // emulating loop for update element
      let endpoint;
      let response;
      let response_chk_arr = [];
      let data;
      let elements = this.attributeList;
      product_id = this.part.id;
      for (let index = 0; index < elements.length; index++) {
        element = elements[index];
        if (element.id) {
          endpoint = `${ApplicationMainHost}/api/product/attribute/${element.id}/`;
          data = {
            attribute_name: element.attribute_name,
            attribute_value: element.attribute_value,
            product: product_id,
          };
          response = await apiService(endpoint, 'PUT', data);
          if (response) {
            this.chkResponse.push(response);
          }
        } else if (element.attribute_value != '') {
          endpoint = `${ApplicationMainHost}/api/product/attribute/`;
          data = {
            attribute_name: element.attribute_name,
            attribute_value: element.attribute_value,
            product: product_id,
          };
          response = await apiService(endpoint, 'POST', data);
          if (response) {
            this.chkResponse.push(response);
          }
        }
      }
      if (this.chkResponse.length > 0) {
        this.successToast('Атрибут сохранен успешно');
      } else {
        this.errorToast('Атрибут не сохранен!');
      }
    },

    // Begin description portion of code
    async getDescription(product_id) {
      const endpoint = `${ApplicationMainHost}/api/product/description/?product_id=${product_id}`;
      let response = await apiService(endpoint);
      if (response.results.length === 0) {
        this.addDescriptionButton = false;
      } else {
        this.editorData = response.results[0].text || null;
        this.descriptionId = response.results[0].id || null;
        this.addDescriptionButton = true;
      }
    },
    async saveDescription() {
      if (this.descriptionId) {
        const id = this.descriptionId;
        const endpoint = `${ApplicationMainHost}/api/product/description/${id}/`;
        const data = {
          text: this.editorData,
          product: this.part.id,
        };
        let response = await apiService(endpoint, 'PUT', data);
        if (response) {
          this.successToast('Описание сохранено успешно');
        } else {
          this.errorToast('Описание не сохранено!');
        }
      }
    },
    async addDescription() {
      const endpoint = `${ApplicationMainHost}/api/product/description/`;
      data = {
        text: this.editorData,
        product: this.part.id,
      };
      const response = await apiService(endpoint, 'POST', data);
      if (response) {
        this.successToast('Описание сохранено успешно');
      } else {
        this.errorToast('Описание не сохранено!');
      }
    },
    // End of description section of code
    errorToast(message) {
      this.$toast.open({
        message: message,
        type: 'error',
        position: 'top-right',
      });
    },
    successToast(message) {
      this.$toast.open({
        message: message,
        type: 'success',
        position: 'top-right',
      });
    },
    popFromArrayById(array, id) {
      let removeIndex = array
        .map(function (item) {
          return item.id;
        })
        .indexOf(id);
      array.splice(removeIndex, 1);
      return array;
    },
    //Video part of code
    async getVideo(product_id) {
      const endpoint = `${ApplicationMainHost}/api/product/videos/?product_id=${product_id}`;
      let response = await apiService(endpoint);
      this.productVideos = response.results;
    },
    async saveVideo(id) {
      if (id) {
        const endpoint = `${ApplicationMainHost}/api/product/videos/${id}/`;
        let getIndex = this.productVideos
          .map(function (item) {
            return item.id;
          })
          .indexOf(id);
        const data = {
          url: this.productVideos[getIndex].url,
          product: this.part.id,
        };
        let response = await apiService(endpoint, 'PUT', data);
      } else {
        this.addVideo();
      }
    },
    async deleteVideo(id) {
      const endpoint = `${ApplicationMainHost}/api/product/videos/${id}/`;
      await apiService(endpoint, 'DELETE');
      this.popFromArrayById(this.productVideos, id);
    },
    async addVideo() {
      const endpoint = `${ApplicationMainHost}/api/product/videos/`;
      data = {
        url: this.productVideoUrl,
        product: this.part.id,
      };
      const response = await apiService(endpoint, 'POST', data);
      if (response) {
        this.productVideos.push(response);
        this.productVideoUrl = null;
        this.successToast('Видео сохранено успешно');
      } else {
        this.errorToast('Видео не сохранено!');
      }
    },

    //Image Part Of Code
    onFileSelected(event) {
      this.selectedFiles = event.target.files;
    },
    async getImage(id) {
      const endpoint = `${ApplicationMainHost}/api/product/images/?product_id=${id}`;
      let response = await apiService(endpoint);
      this.productImages = response.results;
      console.log(response.results)
    },
    async uploadImage() {
      this.imageLoading = true;
      const endpoint = `${ApplicationMainHost}/api/product/images/`;
      let fd = new FormData();
      for (const element of this.selectedFiles) {
        fd.append('image', element, element.name);
      }

      fd.append('product', this.part.id);
      this.imageLoading = true;
      await axiosUploadImageApi(endpoint, fd)
        .then((response) => {
          if (response) {
            this.successToast('Фото сохранено успешно');
            this.imageLoading = false;
            this.selectedFiles = [];
          } else {
            this.errorToast('Фото не сохранилось!');
            this.imageLoading = false;
          }
        })
        .catch((error) => {
          this.imageLoading = false;
        });
    },
    async deleteImage(id) {
      const endpoint = `${ApplicationMainHost}/api/product/images/${id}/`;
      const res = await apiService(endpoint, 'DELETE');
      if (!res) {
        this.successToast('Фото удалено успешно');
      } else {
        this.errorToast('Фото не удалилось!');
      }
      let removeIndex = this.productImages
        .map(function (item) {
          return item.id;
        })
        .indexOf(id);
      this.productImages.splice(removeIndex, 1);
    },
    // Part of product itself
    async editPart() {
      // Отправляем основные данные на сервер
      // Needs to make API and Login in Vue -- Here
      const endpoint = `${ApplicationMainHost}/api/product/detail/${this.part.id}/`;

      //Логика: Если есть выбранный бренд или ед изм то отправляем их
      //или дефолтовые значения
      if (!this.selectedUnitId) {
        unitId = this.part.unit;
      } else {
        unitId = this.selectedUnitId.id;
      }
      //brand
      if (!this.selectedBrandId) {
        brandId = this.part.brand;
      } else {
        brandId = this.selectedBrandId.id;
      }
      //car model
      if (!this.selectedCarModelId) {
        carId = this.part.car_model.id;
      } else {
        carId = this.selectedCarModelId.id;
      }
      //car engine
      if (!this.selectedCarEnginelId) {
        engineId = this.part.engine;
      } else {
        engineId = this.selectedCarEnginelId.id;
      }
      let car_mod = this.value.map((obj) => {
        return obj.id;
      });
      //Lgic of car engine values comprihansion list
      let engine = [];
      if (this.valueEngine.lenght == 0) {
        engine = [];
      }
      engine = this.valueEngine.map((obj) => {
        return obj.id;
      });

      const data = {
        one_c_id: Number(this.part.one_c_id),
        name: this.part.name,
        name2: this.part.name2,
        cat_number: this.part.cat_number,
        oem_number: this.part.oem_number,
        brand: brandId,
        car_model: car_mod,
        unit: unitId,
        active: this.part.active,
        engine: engine,
        product_cross: this.part.product_cross,
      };
      //console.log(JSON.stringify(data));
      let response = await apiService(endpoint, 'PUT', data);
      //console.log(response)
      if (response) {
        this.successToast('Товар сохранен!');
      } else {
        this.errorToast('Ошибка сохранения товара!');
      }
      //window.location.href = `${ApplicationMainHost}/product/`
    },
    async getPartCarModel(id_list) {
      //Gettin car model list for specific car part
      const endpoint = `${ApplicationMainHost}/api/product/selectpartcarmodel/?pk=${id_list}`;
      const data = await apiService(endpoint);
      this.value = data;
    },
    async getPartCarEngine(id_list) {
      let endpoint;
      if (id_list.length === 0) {
        endpoint = `${ApplicationMainHost}/api/product/selectpartcarengine/?pk=0`;
      } else {
        endpoint = `${ApplicationMainHost}/api/product/selectpartcarengine/?pk=${id_list}`;
      }

      const data = await apiService(endpoint);
      this.valueEngine = data;
      return data;
    },
    async getPart(id, car_make_id) {
      const endpoint = `${ApplicationMainHost}/api/product/detail/${id}/`;
      // await this.getAttributeList();
      await this.getAttribute(id);
      const data = await apiService(endpoint);
      this.part = data;
      this.getPartCarModel(this.part.car_model);
      this.getPartCarEngine(this.part.engine);
      await this.getSelectCarModelList(car_make_id); // Here need to implement selecting models by carmake
      // await this.getSelectCarEnginelList(this.part.car_model.id);
      await this.getImage(this.part.id);

      // console.log(data);
    },
    async getSelectCarModelList(id) {
      const endpoint = `${ApplicationMainHost}/api/product/selectlistcarmodel/${id}/`;
      const data = await apiService(endpoint);
      this.selectCarModelList = data;
    },
    async getSelectCarEnginelList(id) {
      const endpoint = `${ApplicationMainHost}/api/product/selectlistcarengine/`;
      const data = await apiService(endpoint);
      this.selectCarEngineList = data;
    },
    async getSelectUnitList() {
      const endpoint = `${ApplicationMainHost}/api/product/selectlistunits/`;
      const data = await apiService(endpoint);
      this.selectUnitList = data;
    },
    async getSelectBrandsList() {
      const endpoint = `${ApplicationMainHost}/api/product/selectlistbrands/`;
      const data = await apiService(endpoint);
      this.selectBrandList = data;
    },
  },
  // beforeMount() {
  //     this.part.id = document.getElementById('mainId').getAttribute('token') || '';
  // },
  created() {
    this.getSelectUnitList();
    this.getSelectBrandsList();
    const id = document.getElementById('mainId').getAttribute('token') || '';
    const car_make_id =
      document.getElementById('car_m_id').getAttribute('token') || '';
    this.getSelectCarEnginelList();
    this.getPart(id, car_make_id);
    this.getVideo(id);
    this.getDescription(id);
    // commenmt
  },
  mounted() {},
});
