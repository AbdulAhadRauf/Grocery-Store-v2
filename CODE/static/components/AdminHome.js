import AdminAnalysis from "./AdminAnalysis.js";

export default {
  template: `
  
<div class="container mt-4">
<h2>Admin Dashboard</h2>

 <div v-if="requests.length > 0">
 <div
   class="card mb-3"
   v-for="request in requests"
   :key="request.request_id"
 >
   <div class="card-body">
     <h5 class="card-title">
       {{ request.request_type.split("_")[0].toUpperCase() }} Request
     </h5>
     <p class="card-text">Requested by: {{ request.username }}</p>
     <button v-if="request.details"  class="btn btn-info" @click="showdetails(request.details, request.request_id)">
       Show Details
     </button>

     <button
       class="btn btn-success"
       v-if="request.request_type.includes('add')"
       @click="handleAction(request.request_id, 'Add')"
     >
       Add
     </button>
     <button
       class="btn btn-primary"
       v-if="request.request_type.includes('update')"
       @click="handleAction(request.request_id, 'Update')"
     >
       Update
     </button>
     <button
       class="btn btn-danger"
       v-if="request.request_type.includes('delete')"
       @click="handleAction(request.request_id, 'Delete')"
     >
       Delete
     </button>
     <button
       class="btn btn-secondary"
       @click="handleAction(request.request_id, 'Reject')"
     >
       Reject
     </button>


     <div
     v-if="showDetailsBoolean && activeRequest && activeRequest.request_id === request.request_id"
     class="mt-3">
     <table class="table table-bordered">
       <thead class="thead-light">
         <tr>
           <th scope="col">Details</th>
           <th scope="col">Values</th>
         </tr>
       </thead>
       <tbody>
         <tr v-for="(value, key) in activeRequest.details" :key="key">
           <td><strong>{{ key }}</strong></td>
           <td>{{ value }}</td>
         </tr>
       </tbody>
     </table>
   </div>
   



   </div>
 </div>
</div>

<div v-else><p>No pending requests.</p></div>

<div class= "d-flex align-items-center justify-content-center">
    <button class="btn btn-lg btn-success mr-5 " @click="gotoAnalysisPage"> See Store Analysis </button>
    <div class= "text ms-2" >{{gotoAnalysisPageMessage}}        </div>

</div>


<div v-if='allusers'>

    <table class="table">
        <thead class="thead-light">
        <tr>
            <th scope="col">#</th>
            <th scope="col">Username</th>
            <th scope="col">Email_address</th>
            <th scope="col">Roles</th>
            <th scope="col">Action</th>
        </tr>
        </thead>


        <tbody v-for="(user, key) in allusers" :key=key :value=user>
            <tr>
            <th scope="row"> {{key}}</th>
            <td>{{user.username}}</td>
            <td>{{user.email_address}}</td>

            <td v-for="(role, name) in user.roles[user.roles.length -1]">{{role}}</td>
            <td v-if= "user.roles[user.roles.length -1]['name']!='admin' "> 
            <button v-bind:class="['btn btn-sm', 'rounded-1', user.active? 'btn-success' : 'btn-danger']" @click="toggleuser(user.email_address, user.username, user.active)"> {{user.active ? 'Deactivate' : 'Activate'}}</button>
            </td>
            <td v-else></td>
            </tr>
        
        </tbody>
    </table>

</div>

</div>
  
  `,
  data() {
    return {
      requests: [],
      activeRequest: null,
      showDetailsBoolean: false,
      auth_token: "",
      adminanalysis: false,
      gotoAnalysisPageMessage:'',
      allusers:{},
    };
  },

  created() {
    this.fetchRequests();
    this.auth_token = localStorage.getItem("auth_token");
    this.getusers();
  },
// TODO: Admin analysis fix the pdf sending part
//TODO : to send mail via pdfkit or render template 


  methods: {
    async toggleuser(mail,name,status){
    
      if( confirm(`Do you want really want to ${status ? 'Deactivate' : 'Activate'} ${name} ?` )){


      try{
        const response = await fetch('/toggleuser', {
          method: "POST", 
          headers:{"Content-Type": "application/json", "Authentication-Token" : this.auth_token},
          body : JSON.stringify({email_address : mail})});
        if(response.ok){
          const data = await response.json();
          console.log(data);
          alert(`${name} has been ${ status ? 'Deactivated' : 'Activated'}`)
        }

      }
      catch(e){console.error(e);}
      finally{ 
        this.getusers()

      }
    }
    },
     async getusers(){
      try{
          const response = await fetch("/user", {method:"GET", headers:{"Authentication-Token" : this.auth_token}})
          
          if(response.ok){
            const data = await response.json();
            this.allusers = {...data}  
          }
          else{
            const data = await response.json();
            console.log(data);
          }

          

      }
      catch (e){
        console.error(e);
      }
    },
    
    gotoAnalysisPage() {
    let count = 5;
    this.gotoAnalysisPageMessage = `Redirecting to Analysis... ${count}`;
    const intervalId = setInterval(() => {
      count--;
      this.gotoAnalysisPageMessage = `Redirecting to Analysis... ${count}`;
      if (count === 0) {
        clearInterval(intervalId);
        this.$router.push({ name: AdminAnalysis});
      }
    }, 1000); 
  },


    showdetails(details, requestId) {
      if (this.activeRequest && this.activeRequest.request_id === requestId) {
        this.showDetailsBoolean = !this.showDetailsBoolean;
      } else {
        this.activeRequest = { details: details, request_id: requestId }; // Now creating an object with details and request_id
        this.showDetailsBoolean = true;
      }
    },

    fetchRequests() {
      fetch("/admin", {
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth_token"),
        },
      })
        .then((response) => response.json())
        .then((data) => {
          this.requests = data;
        })
        .catch((error) => console.error("Error:", error));
    },

    


    handleAction(requestId, action) {
      const requestOptions = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.getItem("auth_token"),
        },
        body: JSON.stringify({ request_id: requestId, what_action: action }),
      };

      fetch("/admin", requestOptions)
        .then((response) => response.json())
        .then((data) => {
          alert(data.message);
          this.fetchRequests();
        })
        .catch((error) => console.error("Error:", error));
    },
    
  },

  filters: {
    json(value) {
      return JSON.stringify(value, null, 2);
    },
  },
};
