export default {
    template: `
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-md-6">
            <div class="registration-form bg-light mt-4 p-4">
              <form class="row g-3" @submit.prevent="registerUser">
                <h4 class =" text-center">Grocery Store V2 - Register</h4>
                <div class="col-12">
                  <label>Username</label>
                  <input type="text" class="form-control" placeholder="Username" v-model="user.username" required>
                </div>
                <div class="col-12">
                  <label>Email address</label>
                  <input type="email" class="form-control" placeholder="Email@example.com" v-model="user.email_address" required>
                </div>
                <div class="col-12">
                  <label>Password</label>
                  <input type="password" class="form-control" placeholder="Password" v-model="user.password" required>
                </div>
                <div class="col-12">
                  <label>Contact Number</label>
                  <input type="tel" class="form-control" placeholder="Contact Number" v-model="user.contact_number" required>
                </div>
                <div class="col-12">
                  <label>Home Address</label>
                  <input type="text" class="form-control" placeholder="Home Address" v-model="user.home_address" required>
                </div>
                <div class="col-12">
                  <button type="submit" class="btn btn-warning float-end">Register</button>
                </div>
              </form>
              <hr class="mt-4">
              <div class="col-12">
                <p class="text-center mb-0">Already have an account? <router-link :to="({name : 'Login'})">  Sign in </router-link></p>
              </div>
            </div>
          </div>
        </div>
      </div>
    `,
    data() {
      return {
        user: {
          username: '',
          email_address: '',
          password: '',
          contact_number: '',
          home_address: ''
        },
        registrationEndpoint: "/user"
      };
    },
    methods: {
      isValidContactNumber() {
      const regex = /^\d+$/;
      return regex.test(this.user.contact_number);
    },


    async registerUser() {
      if (!this.isValidContactNumber()) {
        alert('Please enter a valid contact number (digits only).');
        return;
                 }

        try {
          const response = await fetch(this.registrationEndpoint, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              username: this.user.username,
              email_address: this.user.email_address,
              password: this.user.password,
              contact_number: this.user.contact_number,
              home_address: this.user.home_address
            })
          });
          const data = await response.json();
          if (response.ok) {
            alert('Registration successful!');

            this.$router.push({"name":"Login"})
          } else {
            alert(`Error: ${data.message}`);
          }
        } catch (error) {
          console.error('There was an error registering the user:', error);
          alert('Registration failed. Please try again later.');
        }
      }
    }
  };
  