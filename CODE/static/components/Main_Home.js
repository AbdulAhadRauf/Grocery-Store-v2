import SearchBar from "./SearchBar.js";
import UserHome from "./UserHome.js";
import AdminHome from "./AdminHome.js";
import StoreManager from "./StoreManager.js";
import Carousel from "./Carousel.js";

export default {
template:`
<div>
<Carousel />
<SearchBar />
<UserHome />
</div>

`,
data(){
    return{
        role: localStorage.getItem('role'),
        token: localStorage.getItem('auth_token'),
    };
},

components:{
    SearchBar,
    UserHome,
    Carousel,
    StoreManager,
    AdminHome,
},



}