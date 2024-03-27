export default {
  template: `
    <div class="container mt-5">
    <div class="header text-center">
        <h1>Welcome, {{name}}</h1>
        <p>Your Order History</p>
    </div>
    
    <table class="table table-striped">
        <thead class="thead-dark">
            <tr>
                <th scope="col">#</th>
                <th scope="col">Product Name</th>
                <th scope="col">Quantity</th>
                <th scope="col">Total Amount</th>
                <th scope="col">Purchase Date</th>
            </tr>
        </thead>
        <tbody v-for="(value, key) in this.orderdata" :key=index>
    
            <tr>
                <td>{{key}}</td>
                <td>{{value.item_name}}</td>
                <td>{{value.item_quantity}}</td>
                <td>{{value.item_total}}</td>
                <td>{{value.purchase_date}}</td>
            </tr>
  
        </tbody>
    </table>
    
    <div class="total" style="overflow: auto;">
        <p class="float-end "><strong class='text-success'>Total Amount Spent Last Month: ₹ {{totalprice}}</strong></p>
    </div>

    <div>
    <button class="btn btn-outline-dark" @click ="download">Download</button>
    <button class="btn btn-outline-dark" @click ="mail">Mail</button>
    </div>
</div>
    
    `,
  data() {
    return {
      total: 0,
      authToken: "",
      user_id: "",
      orderdata: {},
    };
  },
  created() {
    this.authToken = localStorage.getItem("auth_token");
    this.fetchUserProfile();
  },
  computed: {
    totalprice() {
      return Object.values(this.orderdata).reduce((total, order) => {
        return total + parseFloat(order.item_total);
      }, 0);
    },
  },
  methods: {
    download(){
        window.print()
    },

    async mail(){
        const response = await fetch(`/user_requested_report/${this.user_id}`, {headers:{"Authentication-Token" : this.authToken}});
        if (response.ok){
            alert("Mail has been sent to you!")
        }
        else{
            alert("Could not send mail")
        }
    },
    async fetchUserProfile() {
      try {
        const response = await fetch("/api/me", {
          method: "GET",
          headers: {
            "Authentication-Token": `${this.authToken}`,
            "Content-Type": "application/json",
          },
        });

        const data = await response.json();

        if (response.ok) {
          this.user_id = data.user_id;
          this.getUserOrders();
        }
      } catch (error) {
        console.error(error);
      }
    },

    async getUserOrders() {
      try {
        const response = await fetch(`/orderhistory/${this.user_id}`);
        if (response.ok) {
          const data = await response.json();
          this.orderdata = { ...data };
        } else if (!response.ok) {
          const data = await response.json();
          this.orderdata = { message: data.message };
        }
      } catch (e) {
        console.error(e);
      }
    },
  },
};
