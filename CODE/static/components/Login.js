export default {
  template: `
<div class="container ">
    <div class="row justify-content-center ">
      <div class="col-md-6 ">
        <div class="login-form bg-light mt-4 p-4 " >
          <form @submit.prevent="login" class="row g-3" >
            <h4>Grocery Store V2</h4>

            <div v-if="this.show_message_boolean"  class="row g-1">
              <div class="col">
              <div class="alert alert-danger" role="alert">
                                {{this.message}}
              </div>
              </div>
            </div>

            <div class="col-12">
              <label>Email</label>
              <input type="email" name="email" class="form-control" placeholder="Email@example.com" v-model="cred.email_address" required>
            </div>

            <div class="col-12">
              <label>Password</label>
              <input type="password" name="password" class="form-control" placeholder="Password" v-model="cred.password" required>
            </div>

            <div class="col-12">
            <button type="submit" class="btn btn-warning float-end">Sign in</button>
            </div>

          </form>

          <hr class="mt-4">

          <div class="col-12">

            <p class="text-center mb-0">
            New to Grocery Store V2? 
            <router-link :to= '({name: "Register"})'>Create your account</router-link>
            
            </p>

            </div>
        </div>
      </div>
    </div>
  </div>

  `,
  data() {
    return {
      cred: { email_address: null, password: null },
      show_message_boolean: false,
      message: null,
    };
  },
  watch:{
    show_message_boolean(newValue){
      if(newValue){
        setTimeout(() => {
          this.show_message_boolean = false;
        }, 2200);
      }
    },
  },
  methods: {
    async login() {
      if (this.cred.email_address && this.cred.password) {
        if (
          this.cred.email_address.includes("@") &&
          this.cred.email_address.includes(".com")
        ) {
          const response = await fetch("/user_login", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": localStorage.getItem("auth_token"),
            },
            body: JSON.stringify(this.cred),
          });

          if (response.ok) {
            const data = await response.json();
            if (data && data.auth_token) {
              localStorage.setItem("auth_token", data.auth_token);
              localStorage.setItem("role", data.role);
              localStorage.setItem("user_id", data.user_id);
              this.$router.push({ name: "Main_Home" });
            }
          } else if (!response.ok) {
            const data = await response.json();
            this.show_message_boolean = true;
            this.message = data.message;

          }
        }
      } else {
        alert("Invalid credentials!");
      }
    },
  },
};
