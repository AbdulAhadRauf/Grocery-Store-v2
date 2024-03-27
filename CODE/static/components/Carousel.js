export default{

    template:`
    <div class='mt-4 mb-3 container'>
    
<!-- carousel -->
<div class="container mb-2" style="max-height: 528px; max-width: 840px">
  <div
    id="carouselExampleAutoplaying"
    class="carousel slide shadow"
    data-bs-ride="carousel"
  >
    <div class="carousel-inner">
      <div class="carousel-item active" data-bs-interval="3000">
      <img
          src="/static/Grocery1.jpg"
          class="d-block w-100 rounded"
          alt="grocery store image 1"
        />
      </div>
      <div class="carousel-item" data-bs-interval="3000">
        <img
          src="/static/Grocery2.jpg"
          class="d-block w-100 rounded"
          alt="grocery store image 2"
        />
      </div>
      <div class="carousel-item" data-bs-interval="3000">
        <img
          src="/static/Grocery3.jpg"
          class="d-block w-100 rounded"
          alt="grocery store image 3"
        />
      </div>
    </div>
    <button
      class="carousel-control-prev"
      type="button"
      data-bs-target="#carouselExampleAutoplaying"
      data-bs-slide="prev"
    >
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Previous</span>
    </button>
    <button
      class="carousel-control-next"
      type="button"
      data-bs-target="#carouselExampleAutoplaying"
      data-bs-slide="next"
    >
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Next</span>
    </button>
  </div>
</div>
    </div>`,

}