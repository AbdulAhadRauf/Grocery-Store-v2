export default{
template:`
<div class = "container" style="overflow: auto;">
 
  
      <!-- Products List -->
      <div>
        <h2>Your Products</h2>
        <ul type="none" class="d-flex justify-content-around" style="display: flex; flex-wrap: wrap;">
        <li v-for="product in products" :key="product.product_id">
          
          <!-- Bootstrap ka card ,arange in horizontla-->
          <div class="card border-secondary mb-3" style="width:18em;">
              <img class="card-img img-thumbnail mb-3 mt-4" :src=product.imageUrl :alt=product.product_name style= "height:150px; width:150px; margin-left: auto; margin-right: auto;">
              <div class="card-footer d-flex justify-content-around align-items-stretch">
                <h5 class="card-title mt-1">{{product.product_name}}</h5>

                <button class="btn btn-success" @click="setEditProduct(product)">Edit</button>
            <button class="btn btn-primary" @click="deleteProduct(product.product_id)">Delete</button>
              </div>
            </div>
          <!--End  Bootstrap ka card ,arange in horizontla-->
          </li>
        </ul>
      </div>
    

      <!-- Edit Product Form -->
                      <div v-if="editProduct">
                      <h2>Edit Product</h2>
                      <form @submit.prevent="updateProduct" class="p-3">
                  
                          <!-- First rwo me = Name, Price, Quantity, Category-->
                          <div class="row g-3">
                              <div class="col-md-3">
                                  <label for="productName" class="form-label">Product Name</label>
                                  <input v-model="editProduct.product_name" class="form-control" id="productName" placeholder="Product Name" required>
                              </div>
                  
                              <div class="col-md-3">
                                  <label for="productPrice" class="form-label">Product Price</label>
                                  <input v-model="editProduct.product_price" type="number"  min="0" class="form-control" id="productPrice" placeholder="Product Price" required>
                              </div>
                  
                              <div class="col-md-3">
                                  <label for="stockQuantity" class="form-label">Stock Quantity</label>
                                  <input v-model="editProduct.stock_quantity" type="number" min="0" class="form-control" id="stockQuantity" placeholder="Stock Quantity" required>
                              </div>
                  
                              <div class="col-md-3">
                                  <label for="category" class="form-label">Category</label>
                                  <select v-model="editProduct.category_id" class="form-select" id="category" required>
                                      <option v-for="category in categories" :value="category.category_id" :key="category.category_id">
                                          {{ category.category_name }}
                                      </option>
                                  </select>
                              </div>
                          </div>
                  
                          <!--  Manufacture Date, Expiry Date, Image URL -->
                          <div class="row g-3 mt-3">
                              <div class="col-md-4">
                                  <label for="manufactureDate" class="form-label">Manufacture Date</label>
                                  <input v-model="editProduct.manufacture_date" type="datetime-local" class="form-control" id="manufactureDate" required>
                              </div>
                  
                              <div class="col-md-4">
                                  <label for="expiryDate" class="form-label">Expiry Date</label>
                                  <input v-model="editProduct.expiry_date" type="datetime-local" class="form-control" id="expiryDate" required>
                              </div>
                  
                              <div class="col-md-4">
                                  <label for="imageUrl" class="form-label">Image URL</label>
                                  <input v-model="editProduct.imageUrl" class="form-control" id="imageUrl" placeholder="Image URL" required>
                              </div>
                          </div>
                  
                          <!-- Buttons -->
                          <div class="mt-3">
                              <button type="submit" class="btn btn-primary">Update Product</button>
                              <button @click="resetEditForms" type="button" class="btn btn-secondary">Cancel</button>
                          </div>
                  
                      </form>
                  </div>



      <button class= "btn btn-success float-end me-4" @click="showYouAddProductForm"> Add New Product</button>


                        <!-- Add Product Form -->
                        <div v-if="showAddProductForm">
                      <h2>Add New Product</h2>
                      <form @submit.prevent="addProduct" class="p-3">

                          <!-- First Row: Name, Price, Quantity, Category -->
                          <div class="row g-3">
                              <div class="col-md-3">
                                  <label for="newProductName" class="form-label">Product Name</label>
                                  <input v-model="newProduct.product_name" class="form-control" id="newProductName" placeholder="Product Name" required>
                              </div>

                              <div class="col-md-3">
                                  <label for="newProductPrice" class="form-label">Product Price</label>
                                  <input v-model="newProduct.product_price" type="number" min="0" class="form-control" id="newProductPrice" placeholder="Product Price" required>
                              </div>

                              <div class="col-md-3">
                                  <label for="newStockQuantity" class="form-label">Stock Quantity</label>
                                  <input v-model="newProduct.stock_quantity" type="number" min="0" class="form-control" id="newStockQuantity" placeholder="Stock Quantity" required>
                              </div>

                              <div class="col-md-3">
                                  <label for="newCategory" class="form-label">Category</label>
                                  <select v-model="newProduct.category_id" class="form-select" id="newCategory" required>
                                      <option v-for="(name, id) in allCats" :key="id" :value="id">
                                          {{ name }}
                                      </option>
                                  </select>
                              </div>
                          </div>

                          <!-- Second row start-->
                          <div class="row g-3 mt-3">
                              <div class="col-md-4">
                                  <label for="newManufactureDate" class="form-label">Manufacture Date</label>
                                  <input v-model="newProduct.manufacture_date" type="datetime-local" class="form-control" id="newManufactureDate" required>
                              </div>

                              <div class="col-md-4">
                                  <label for="newExpiryDate" class="form-label">Expiry Date</label>
                                  <input v-model="newProduct.expiry_date" type="datetime-local" class="form-control" id="newExpiryDate" required>
                              </div>

                              <div class="col-md-4">
                                  <label for="newImageUrl" class="form-label">Image URL</label>
                                  <input v-model="newProduct.imageUrl" class="form-control" id="newImageUrl" placeholder="/static/ImageName.png" required>
                              </div>
                          </div>

                          <div class="mt-3">
                              <button type="submit" class="btn btn-primary">Add Product</button>
                          </div>

                      </form>
                  </div>







                      <!-- Categories List -->
                      <div>
                        <h2>Your Categories</h2>
                        <ul type="none" class="d-flex justify-content-around" style="display: flex; flex-wrap: wrap;">
                          <li v-for="category in categories" :key="category.category_id">
                              <div class="card border-secondary mb-3" style="width: 18rem;">
                                <div class="card-header"><h5>{{ category.category_name }}</h5></div>
                                <div class="card-body text-dark d-flex justify-content-between">
                                <button class="btn btn-success" @click="setEditCategory(category)">Edit</button>
                                <button class="btn btn-warning" @click="exportcat(category.category_name,category.category_id)">Get Csv</button>
                                <button class="btn btn-danger" @click="deleteCategory(category.category_id)">Delete</button>
                                </div>
                              </div>
                          </li>
                        </ul>
                      </div>
                  

                                      <!-- Edit Category Form -->
                                      <div v-if="editCategory">
                                          <h2>Edit Category</h2>
                                          <form @submit.prevent="updateCategory" class="p-3">
                                      
                                              <!-- Input Group for Category Name and Buttons -->
                                              <div class="input-group mb-3">
                                                  <input v-model="editCategory.category_name" type="text" class="form-control" placeholder="New Category Name" aria-label="New Category Name" required>
                                                  
                                                  <button type="submit" class="btn btn-primary">Update Category</button>
                                                  <button @click="resetEditForms" type="button" class="btn btn-secondary">Cancel</button>
                                              </div>
                                      
                                              <!-- Hidden Inputs -->
                                              <input v-model="editCategory.old_category_name" type="hidden">
                                              <input v-model="editCategory.category_id" type="hidden">
                                      
                                          </form>
                                      </div>
                                      
                                      <button class= "btn btn-success mb-2 float-end me-4" @click="showYouAddCategoryForm" > Add New Category</button>
      
                                      <!-- Add Category Form -->
                                      <div v-if="showAddCategoryForm">
                                          <h2>Add New Category</h2>
                                          <form @submit.prevent="addCategory" class="p-3">
                                      
                                              <!-- Input Group for Category Name and Submit Button -->
                                              <div class="input-group mb-3">
                                                  <input v-model="newCategory.category_name" type="text" class="form-control" id="categoryName" placeholder="Category Name" aria-label="Category Name" required>
                                                  <button type="submit" class="btn btn-primary">Add Category</button>
                                              </div>
                                      
                                          </form>
                                      </div>
                                      





 </div>
`,
data() {
    return {
      allCats :{},
      products: [],
      categories: [],
      showAddProductForm: false,
      showAddCategoryForm: false,
      newProduct: this.getEmptyProduct(),
      newCategory: { category_name: '' },
      editProduct: null,
      editCategory: null,
    };
  },

  created() {
    this.fetchProducts();
    this.fetchCategories();
    this.fetchAllCategories();
  },

  methods: {
    async fetchAllCategories(){
      try{
      const response  = await fetch("/search", { headers: { 'Content-Type': 'application/json',
      "Authentication-Token": localStorage.getItem("auth_token")}});
      if(response.ok){  
      const data = await response.json();
      for (let category of data) {
        this.allCats[category.category_id] = category.category_name;   }
      }
    }
      catch (error){
        console.error(error);
      }

    },
    
    showYouAddProductForm() {
      this.showAddProductForm = !this.showAddProductForm;
    },
    showYouAddCategoryForm() {

      this.showAddCategoryForm = !this.showAddCategoryForm;
    },
    getEmptyProduct() {
      return {
        product_name: '',
        product_price: null,
        stock_quantity: null,
        category_id: null,
        imageUrl: '',
        manufacture_date: '',
        expiry_date: ''
      };
    },

    async fetchProducts() {
      try {
        const creatorId = localStorage.getItem("user_id");
        const response = await fetch(`/user/${creatorId}/products`, { headers: { 'Content-Type': 'application/json',
        "Authentication-Token": localStorage.getItem("auth_token")}});
        if (!response.ok) {
          throw new Error("Failed to fetch products");
        }
        this.products = await response.json();
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    },

    async fetchCategories() {
      try {
        const creatorId = localStorage.getItem("user_id");
        const response = await fetch(`/user/${creatorId}/categories`, { headers: { 'Content-Type': 'application/json',
        "Authentication-Token": localStorage.getItem("auth_token")}});
        if (!response.ok) {
          throw new Error("Failed to fetch categories");
        }
        this.categories = await response.json();
      } catch (error) {
        console.error("Error fetching categories:", error);
      }
    },

    async addProduct() {
        try {
          const creatorId = localStorage.getItem("user_id");
          if (!creatorId) {
            throw new Error("User ID not found in localStorage");
          }
          const response = await fetch('/products', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json',
          "Authentication-Token": localStorage.getItem("auth_token")},
            body: JSON.stringify({ ...this.newProduct})
          });
        
          
          if(response.ok){
            const data = await response.json();
            alert(data.message);
          }
          else if (!response.ok) {
            const data = await response.json();
            alert(data.message)
            throw new Error('Failed to add product');
          }
       
     
        } catch (error) {
          console.error("Error adding product:", error);
          // Handle the error
        }
      },
      async addCategory() {
        try {
          const response = await fetch('/categories', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json',
            "Authentication-Token": localStorage.getItem("auth_token") },
            body: JSON.stringify(this.newCategory)
          });
          if(response.ok){
            const data = await response.json();
            alert(data.message)
          }
          else {
            const data = await response.json();
            alert(data.message);
          }
        } catch (error) {
          console.error("Error adding category:", error);
        }
      },
      async updateProduct() {
        try {
          const response = await fetch(`/products`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json',"Authentication-Token": localStorage.getItem("auth_token") },
            body: JSON.stringify(this.editProduct)
          });
          
          if(response.ok){
            const data = await response.json();
            alert(data.message);
          }
          else if (!response.ok) {
            const data = await response.json();
            alert(data.message)
            throw new Error('Failed to add product');
          }
        } catch (error) {
          console.error("Error updating product:", error);
        }
      },
      async updateCategory() {
        try {
          const response = await fetch(`/categories/${this.editCategory.category_id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' ,"Authentication-Token": localStorage.getItem("auth_token")},
            body: JSON.stringify(this.editCategory)
          });
          if(response.ok){
            const data = await response.json();
            alert(data.message);
          }
          else if (!response.ok) {
            const data = await response.json();
            alert(data.message)
            throw new Error('Failed to add product');
          }
        } catch (error) {
          console.error("Error updating category:", error);
        }
      },
      async deleteProduct(productId) {
        if(confirm('Are you sure you want to delete this product?')) {
          try {
            const response = await fetch(`/products/${productId}`, { 
              method: 'DELETE' ,
               headers: {"Authentication-Token": localStorage.getItem("auth_token")}}
               );
            if(response.ok){
              const data = await response.json();
              alert(data.message);
            }
            else if (!response.ok) {
              const data = await response.json();
              alert(data.message)
              throw new Error('Failed to add product');
            }
            this.products = this.products.filter(p => p.product_id !== productId);
          } catch (error) {
            console.error("Error deleting product:", error);
          }
        }
      },exportcat(categname, categid){
        const authtoken = localStorage.getItem("auth_token");
        fetch(`http://127.0.0.1:5000/create_csv/${categid}`,{
          method: "GET",
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token":authtoken
            },
          }).then((response)=>{
            if (response.ok){
              alert(`An email containing a csv for ${categname} has been sent to you.`)
            }
          }).catch((error)=>{
            alert("Server error please try again later")
          })
            
  
  
      },
  
      async deleteCategory(categoryId) {
        if(confirm('Are you sure you want to delete this category?')) {
          try {
            const response = await fetch(`/categories/${categoryId}`, { method: 'DELETE' , headers:{"Authentication-Token": localStorage.getItem("auth_token")}});
            if(response.ok){
              const data = await response.json();
              alert(data.message);
            }
            else if (!response.ok) {
              const data = await response.json();
              alert(data.message)
              throw new Error('Failed to add product');
            }
            this.categories = this.categories.filter(c => c.category_id !== categoryId);
          } catch (error) {
            console.error("Error deleting category:", error);
          }
        }
      },
      resetEditForms() {
        this.editProduct = null;
        this.editCategory = null;
      },
      setEditProduct(product) {
        this.editProduct = { ...product };
      },
  
      setEditCategory(category) {
        this.editCategory = { ...category, old_category_name: category.category_name };
      }
    }
  };