export default {
  template: `
    <div class="container mt-4" id="cart">
      <h2>Your Shopping Cart</h2>
      <div v-if="cartItems.length > 0">
        <table class="table">
          <thead>
            <tr>
              <th scope="col">Item</th>
              <th scope="col">Quantity</th>
              <th scope="col">Price</th>
              <th scope="col">Total</th>
              <th scope="col">Remove Quantity</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in cartItems" :key="item.cart_id">
              <td>{{ item.item_name }}</td>
              <td>{{ item.item_quantity }}</td>
              <td>\${{ item.item_total / item.item_quantity }}</td>
              <td>\${{ item.item_total }}</td>
              <td>
                <input type="number" v-model.number="item.removeQuantity" min="1" :max="item.item_quantity" class="form-control">
              </td>
              <td>
                <button class="btn btn-danger btn-sm" @click="removeFromCart(item.product_id, item.removeQuantity)">Remove</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="text-right">
          <h4>Total: \${{ total.toFixed(2) }}</h4>
          <button class="btn btn-primary" @click="placeOrder">Place Order</button>
        </div>
      </div>
      <div v-else>
        <p>Your cart is empty.</p>
      </div>
    </div>
  `,
  data() {
    return {
      cartItems: [],
      total: 0,
    };
  },
  created() {
    this.fetchCartItems();
  },
  methods: {
    fetchCartItems() {
      fetch('/cart', { headers: { 'Content-Type': 'application/json',
      "Authentication-Token": localStorage.getItem("auth_token")}})
        .then(response => response.json())
        .then(data => {
          this.cartItems = data.flatMap(cart => cart.cart_items).map(item => ({
            ...item,
            removeQuantity: 1  // Initialize removeQuantity with 1
          }));
          this.calculateTotal();
        })
        .catch(error => {
          console.error('Error fetching cart items:', error);
        });
    },
    removeFromCart(productId, removeQuantity) {
      fetch('/cart', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          "Authentication-Token": localStorage.getItem("auth_token"),
        },
        body: JSON.stringify({ product_id: productId, quantity: removeQuantity })
      })
      .then(response => response.json())
      .then(data => {
        alert(data.message);
        this.fetchCartItems();  // Refresh the cart items
      })
      .catch(error => {
        console.error('Error removing item from cart:', error);
      });
    },
    calculateTotal() {
      this.total = this.cartItems.reduce(
        (acc, item) => acc + item.item_total, 0
      );
    },
    placeOrder() {
      fetch('/checkout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          "Authentication-Token": localStorage.getItem("auth_token"),
        }
      })
      .then(response => response.json())
      .then(data => {
        alert('Order placed successfully!');
        this.cartItems = [];  // Clear the cart items
        this.total = 0;
      })
      .catch(error => {
        console.error('Error placing order:', error);
      });
    }
  },
};
