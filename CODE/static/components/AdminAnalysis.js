export default {
    template:` 
    
    <div>
    <div class=" container d-flex justify-content-center  bg-dark text-white p-3 mb-2" style="height: 80px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);">
        <h2 class="mb-0">PREVIOUS ANALYSIS</h2>
    </div>

    <div class="container">
        <div class="row g-3">
            <div class="col-md-6">
                <div class="card border-success">
                    <div class="card-header bg-success text-white text-center">
                        Pie Chart <br />by Category
                    </div>
                    <img src="static/pchart_category.png" alt="pchart category" class="card-img-top">
                </div>
            </div>

            <div class="col-md-6">
                <div class="card border-success">
                    <div class="card-header bg-success text-white text-center">
                        Pie Chart <br />by Items
                    </div>
                    <img src="static/pchart_items.png" alt="pchart items" class="card-img-top">
                </div>
            </div>

            <div class="col-md-6">
                <div class="card border-success">
                    <div class="card-header bg-success text-white text-center">
                        Daily <br />Sales
                    </div>
                    <img src="static/daily_sales.png" alt="daily sales" class="card-img-top">
                </div>
            </div>

            <div class="col-md-6">
                <div class="card border-success">
                    <div class="card-header bg-success text-white text-center">
                        Cumulative <br />Revenue
                    </div>
                    <img src="static/cumulative_revenue.png" alt="cumulative revenue" class="card-img-top">
                </div>
            </div>
        </div>
        
        <!--button placement at bottom ?????? -->
        <div class="d-flex justify-content-end mt-3">
        <button class="btn btn-info mx-2" @click="downloadanalysis">Download Analysis</button>
        <button class="btn btn-info mx-2" @click="showanalysis">Generate New Analysis and Mail </button>
        </div>
    </div>
</div>
`,
//TODO:2 buttons,  mail or print ?
  methods:{
    // showanalysis sends thee analysis via mail 
    //downloadanalysis
    downloadanalysis(){
        window.print()
    },

    showanalysis() { 
        fetch("/analysis", {
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": localStorage.getItem("auth_token"),
          },
        })
        .then((response) => response.json()).then(data=>{alert(data.message)}).catch(() => alert("An error occurred while initiating the analysis"));
      },
    
  }

}