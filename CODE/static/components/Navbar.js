export default {
  template: `<div>
  <nav class="navbar navbar-expand-lg mb-2 py-3 d-flex align-items-center " style="  ;background-color:#94d2bd;">
      <div class="container-fluid">
          <a class="navbar-brand" href="#">Grocery Store V-2.0</a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" 
                  data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" 
                  aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
              <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                  <li class="nav-item" v-if="role=='user' || role=='admin' || role =='manager' " >
                      <router-link   class="nav-link" :to="{ name: 'Main_Home' }">Home</router-link>
                  </li>
                  <li class="nav-item" v-if="role=='admin'" >
                      <router-link class="nav-link"   :to="{ name: 'AdminHome' }">Admin Home</router-link>
                  </li>
                  <li class="nav-item" v-if="role === 'admin' || role === 'manager'" >
                      <router-link class="nav-link"   :to="{ name: 'StoreManager' }">Manager Home</router-link>
                  </li>
              </ul>
              <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                  <li class="nav-item" v-if="!this.token">
                  <router-link class="nav-link" :to="{ name: 'Login' }">Login</router-link>
                  </li>
                  <li class="nav-item" v-if="!this.token">
                  <router-link class="nav-link" :to="{ name: 'Register' }">Register</router-link>
                  </li>
                  <li class="nav-item" v-if="this.token">
                      <router-link class="nav-link" :to="{ name: 'Profile' }">Profile</router-link>
                  </li>
                  <li class="nav-item" v-if="this.token" >
                      <router-link class="nav-link" :to="{ name: 'Cart' }">Cart</router-link>
                  </li>
                  <li class="nav-item" v-if="this.token">
                      <router-link class="nav-link" :to="{ name: 'Logout' }">Logout</router-link>
                  </li>
              </ul>
          </div>
      </div>
  </nav>
</div>`,
  data(){
    return{
        token: '',
        role : '' ,
    }
  },
  created(){
    this.token= localStorage.getItem("auth_token");
    this.role = localStorage.getItem("role");
  },
}
