export default {
  template: `

      <div class="container">
        <div class="row justify-content-center">
          <div class="col-md-6">
            <div class="profile-form bg-light mt-4 p-4">
              <h4>Grocery Store V2 - Profile</h4>
              
              <!-- Update Password Form -->
              <form class="row g-3 mb-4" @submit.prevent="updatePassword">
                <div class="col-12">
                  <label for="oldPassword">Old Password</label>
                  <input type="password" class="form-control" id="oldPassword" placeholder="Old Password" v-model="credentials.old_password" required>
                </div>
                <div class="col-12">
                  <label for="newPassword">New Password</label>
                  <input type="password" class="form-control" id="newPassword" placeholder="New Password" v-model="credentials.new_password" required>
                </div>
                <div class="col-12">
                  <button type="submit" class="btn btn-warning float-end">Update Password</button>
                </div>
              </form>
  
              <!-- Delete Account Section -->
            <h4>Delete Account</h4>
            <form class="row g-3" @submit.prevent="confirmDelete">
              <div class="col-12">
                <label for="username">Username</label>
                <input type="text" class="form-control" id="username" placeholder="Username" v-model="deleteCredentials.username" required>
              </div>
              <div class="col-12">
                <label for="emailAddress">Email Address</label>
                <input type="email" class="form-control" id="emailAddress" placeholder="Email Address" v-model="deleteCredentials.email_address" required>
              </div>
              <div class="col-12">
                <label for="deletePassword">Password</label>
                <input type="password" class="form-control" id="deletePassword" placeholder="Password" v-model="deleteCredentials.password" required>
              </div>
              <div class="col-12">
                <button type="submit" class="btn btn-danger float-end">Delete Account</button>
              </div>
            </form>
            <div class="row" v-if="this.role=='user'">
              <div class="manager-application-form bg-light mt-4 p-4 d-flex justify-content-between" >
                <h4 >Apply for Store Manager Role</h4>
                <button class="btn btn-primary" @click="applyForManager">Apply</button>
                
                </div>
                
                </div>

                <div class = "d-flex align-items-center justify-content-start">
                <router-link :to="({name:'UserAnalysis'})" class="btn btn-outline-dark mx-3"> History </router-link>
                <div class= "font-weight-bold" >See your Order History</div >
                </div>



            </div>
          </div>
        </div>
      </div>
    `,
  data() {
    return {
      authToken : localStorage.getItem("auth_token"),
      role : localStorage.getItem("role"),
      credentials: {
        email_address: "", 
        old_password: "",
        new_password: "",
      },
      deleteCredentials: {
        username: "",
        email_address: "",
        password: "",
      },
      managerApplicationMessage: "",
    };
  },

  created() {
    this.fetchUserProfile();
  },

  methods: {
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
          this.credentials.email_address = data.email_address;
        } else {
          alert(`Error: ${data.message}`);
        }
      } catch (error) {
        console.error("There was an error fetching the user profile:", error);
        alert("Failed to fetch user profile. Please try again later.");
      }
    },

    async updatePassword() {
      try {

        const response = await fetch("/user", {
          method: "PUT",
          headers: {
            "Authentication-Token": `${this.authToken}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email_address: this.credentials.email_address,
            old_password: this.credentials.old_password,
            new_password: this.credentials.new_password,
          }),
        });
        const data = await response.json();
        if (response.ok) {
          alert("Password updated successfully!");
          this.$router.push({ name: "Login" });
         
        } else {
          alert(`Error: ${data.message}`);
        }
      } catch (error) {
        console.error("There was an error updating the password:", error);
      }
    },

    confirmDelete() {
      if (
        confirm(
          "Please confirm you want to delete your account. This action cannot be undone."
        )
      ) {
        this.deleteAccount();
      }
    },

    async deleteAccount() {

      try{
      const response = await fetch("/user", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": `${this.authToken}`,
        },
        body: JSON.stringify({
          username: this.deleteCredentials.username,
          email_address: this.deleteCredentials.email_address,
          password: this.deleteCredentials.password,
        }),
      });

      const data = await response.json();
      if (response.ok) {
        alert("Account deleted successfully!");
        this.$router.push({ name: "Main_Home" });}
      else{
        alert(data.message);
      }
      }

      catch (error){
          console.log(error)
      }
        
    },

    async applyForManager() {
      try {
        const response = await fetch("/BecomeStoreManger", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": `${this.authToken}`,
          },
        });

        const data = await response.json();
        if (response.ok) {
          alert(data.message);
        } else {
          
          alert(data.message)
        }
      } catch (error) {
        console.error("Error during manager application:", error);
        this.managerApplicationMessage = `Error: ${error.message || error}`;
      }
    },
  },
};
