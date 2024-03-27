export default {
  template: `  
  <div class="container">
  <div class="row justify-content-center mt-4">
    <div class="col-md-8">
      <div class="input-group mb-3">
        <input
          type="text"
          class="form-control border-secondary"
          placeholder="Search for products or categories or price"
          v-model="searchString"
        />
        <select class="custom-select" v-model="searchType">
          <option value="Product">Product</option>
          <option value="Category">Category</option>
          <option value="Price">Price</option>
        </select>
        <button class="btn btn-outline-dark" type="button" @click="search">
          Search
        </button>

        <button type="button"  @click="closesearch" class="btn btn-outline-secondary dropdown-toggle dropdown-toggle-split" data-bs-toggle="dropdown" aria-expanded="false">
        <span class="visually-hidden">Toggle Dropdown</span>
      </button>
    

      

      </div>
      <!-- Search styling finishes -->

      <div v-if="closesearchbool" class="d-flex justify-content-around" style="display: flex; flex-wrap: wrap;">
  


      <div v-if="categories.length > 0">
        <div
          v-for="category in categories"
          :key="category.category_id"
          class="mb-5">
          
          <h4>{{ category.category_name }}</h4>
          <div class="row">
            <div
              v-for="product in category.linked_products"
              :key="product.product_id"
              class="col-md-4 mb-4"
            >
              <!-- Product Card -->

              <div class="card">
              <div class="row g-3 ms-3">
                <div class="col-6 d-flex justify-content-center align-items-center">
                  
                <img :src="product.imageUrl" class="card-img img-thumbnail rounded-circle " :alt="product.product_name" />
               
                </div>

                <div class="col-6 d-flex flex-column">
                  <!-- Using flex-column to organize the content in a column and align-items-start to align items to the start of the column -->
                  <div class="card-body d-flex flex-column justify-content-between">
                    <div>
                      <h5 class="card-title text-end">{{ product.product_name }}</h5>
                      <p class="card-text text-end">₹{{ product.product_price }}</p>
                    </div>
                    <div class="mt-3"> 
                      <div class="mb-2">
                        <input type="number" v-model.number="product.quantity"
                         min="1" class="form-control"  placeholder="Quantity" value="1" />
                      </div>
                      <button @click="addToCart(product.product_id, product.quantity)" class="btn btn-outline-success">
                        Add to Cart
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            

              <!-- Product Card -->
            </div>
          </div>
        </div>
      </div>
      
      <div>
        <p v-if="searchMessage">{{ searchMessage }}</p>
      </div>
    </div>
    </div>
  </div>
</div>

  `,

  data() {
    return {
      closesearchbool:true,
      searchString: "",
      searchType: "Product",
      searchResults: [],
      searchMessage: "",
      categories: [],
    };
  },
watch:{
  closesearch(){
    this.closesearchbool
  },
  
  searchMessage(newValue){
    if (newValue){
      setTimeout(() => {
        this.searchMessage = ''
      }, 2000);
    }
  },
},
  methods: {
    closesearch(){
      this.closesearchbool = !this.closesearchbool;
    },
    async search() {
      if (!this.searchString) {
        this.searchMessage = "Please enter a Search query";
        return;
      }

      const endpoint = `/search/${encodeURIComponent(
        this.searchString
      )}?searchneighbourbutton=${this.searchType}`;

      try {
        const response = await fetch(endpoint, { method: "GET" , headers: { 'Content-Type': 'application/json',
        "Authentication-Token": localStorage.getItem("auth_token")}});
        if (response.ok) {
          const data = await response.json();
          this.categories = data;
        } else {
          const errorData = await response.json();
          throw new Error(
            errorData.description || "Error occurred during the search."
          );
        }
      } catch (error) {
        this.searchMessage = `Search failed: ${error.message}`;
      }
    },

    addToCart(productId, quantity) {
      fetch("/cart", {
        method: "POST",
        headers: {
          "Content-Type": "application/json","Authentication-Token": localStorage.getItem("auth_token")
        },
        body: JSON.stringify({ product_id: productId, quantity: quantity }),
      })
        .then((response) => response.json())
        .then((data) => {alert(data.message)
        console.log(data);})
        .catch((error) => console.error("Error adding item to cart:", error));
    },
  },
};
