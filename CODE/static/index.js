import router from "./router.js";
import Navbar from "./components/Navbar.js";

router.beforeEach((to, from, next) => {
    if (!localStorage.getItem('auth_token') && to.name !== 'Login' && to.name !== 'Register') {
        next({ name: 'Login' });
    } else {
        next();
    }
});

new Vue({
    el: "#app",
    router: router,
    components: {
        Navbar,
    },
    data() {
        return {
            has_changed: true,
            token: null,
            role: null,
        };
    },
    created() {
        this.updateAuthDetails();
    },
    watch: {
        $route(to, from) {
            this.has_changed = !this.has_changed;
            this.updateAuthDetails();
        },
        token(newToken, oldToken) {
            this.token = newToken;
        },
        role(newRole, oldRole) {
            this.role = newRole;
        }
    },
    methods: {
        updateAuthDetails() {
            this.token = localStorage.getItem("auth_token");
            this.role = localStorage.getItem('role');
        }
    },
    template: `
        <div>
            <Navbar :key="has_changed" ></Navbar>
            <router-view></router-view>
        </div>
    `,
});
