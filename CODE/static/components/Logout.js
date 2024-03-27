export default {
  template: `<div></div>`,
  mounted() {
    fetch("http://127.0.0.1:5000/user_logout", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token" : localStorage.getItem("auth_token")
      },
    }).then((response) => {
      if (response.ok) {
        localStorage.removeItem("auth_token");
        localStorage.removeItem("role");
        localStorage.removeItem("user_id");

        this.$router.push({ name: "Login" });
      }
    });
  },
};
