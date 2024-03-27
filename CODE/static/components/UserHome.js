export default {
    template: ` <div class="container mt-4">
    <h1>Products</h1>
    
    <div v-for="category in categories" :key="category.category_id" class="mb-5">
      <h4>{{ category.category_name }}</h4>
      <div class="row">
        <div v-for="product in category.linked_products.reverse()" :key="product.product_id" class="col-md-4 mb-4">
        
        <div class="card">
            <img :src="product.imageUrl" class="card-img-top rounded-bottom-5 rounded-top-3 shadow" style=" margin-left: auto; margin-right: auto;" :alt="product.product_name">
          
            <div class="card-body d-flex flex-column justify-content-between">
              <div>
                <!-- Product name and price in one line with space between -->
                <div class="d-flex justify-content-between align-items-center mt-4 px-1">
                  <h5 class="card-title">{{ product.product_name }}</h5>
                  <p class="card-text">₹{{ product.product_price }}</p>
                </div>
              </div>

              <div class="d-flex justify-content-between align-items-center input-group mt-4 mb-1 px-2">
                <input type="number" v-model.number="product.quantity" min="1" class="form-control" placeholder="Quantity" value="1">
                <button @click="addToCart(product.product_id, product.quantity)" class="btn btn-outline-success">Add to Cart</button>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
    `,
    data() {
      return {
        categories: [],
      };
    },
    created() {
      this.fetchProducts();
    },
    methods: {
      fetchProducts() {
        fetch('/search', { headers: { 'Content-Type': 'application/json',
        "Authentication-Token": localStorage.getItem("auth_token")}})
          .then(response => response.json())
          .then(data => {
            this.categories = data;
        
            
          })
          .catch(error => console.error('Error fetching products:', error));
      },
      addToCart(productId, quantity) {
        fetch('/cart', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            "Authentication-Token": localStorage.getItem("auth_token")
          },
          body: JSON.stringify({ product_id: productId, quantity: quantity }),
        })
        .then(response => response.json())
        .then(data => alert(`${data.message}`))
        .catch(error => console.error('Error adding item to cart:', error));

        
      },
      gotocart(){
        this.$router.push({name:"Cart"})
      }
    }
  };
  