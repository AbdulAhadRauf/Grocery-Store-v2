import Login from "./components/Login.js";
import Logout from "./components/Logout.js";
import Register from "./components/Register.js";
import Profile from "./components/Profile.js";
import SearchBar from "./components/SearchBar.js";
import Cart from "./components/Cart.js";
import Main_Home from "./components/Main_Home.js";
import UserHome from "./components/UserHome.js";
import StoreManager from "./components/StoreManager.js";
import AdminHome from "./components/AdminHome.js";
import PageNotFound from "./components/PageNotFound.js";
import AdminAnalysis from "./components/AdminAnalysis.js";
import UserAnalysis from "./components/UserAnalysis.js";

const routes = [
  {
    path: "/useranalysis",
    name: "UserAnalysis",
    component: UserAnalysis,
  },
  {
    path: "*",
    name: "PageNotFound",
    component: PageNotFound,
  },
  {
    path: "/adminanalysis",
    name: AdminAnalysis,
    component: AdminAnalysis,
  },
  {
    path: "/userhome",
    component: UserHome,
    name: "UserHome",
  },

  {
    path: "/storemanager",
    component: StoreManager,
    name: "StoreManager",
  },
  {
    path: "/adminhome",
    component: AdminHome,
    name: "AdminHome",
  },
  {
    path: "/",
    component: Main_Home,
    name: "Main_Home",
  },
  {
    path: "/cart",
    component: Cart,
    name: "Cart",
  },
  {
    path: "/searchbar",
    component: SearchBar,
    name: "SearchBar",
  },
  {
    path: "/user_login",
    component: Login,
    name: "Login",
  },
  {
    path: "/user_logout",
    component: Logout,
    name: "Logout",
  },
  {
    path: "/register",
    component: Register,
    name: "Register",
  },
  {
    path: "/profile",
    component: Profile,
    name: "Profile",
  },
];

export default new VueRouter({
  routes,
});
