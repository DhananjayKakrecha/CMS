const API_BASE = "http://localhost:8000/api";

document.getElementById("loginForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const res = await fetch(`${API_BASE}/auth/login/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
        });

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.detail || "Login failed");
        }

        // Store email temporarily for OTP step
        localStorage.setItem("otp_email", email);

        window.location.href = "/otp/";
    } catch (err) {
        document.getElementById("error").innerText = err.message;
    }
});

document.getElementById("otpForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const otp = document.getElementById("otp").value;
    const email = localStorage.getItem("otp_email");

    if (!email) {
        window.location.href = "/login/";
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/auth/verify-otp/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, otp }),
        });

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.detail || "OTP verification failed");
        }

        // Store JWT
        localStorage.setItem("access_token", data.tokens.access);
        localStorage.setItem("refresh_token", data.tokens.refresh);
        localStorage.removeItem("otp_email");

        // Decode JWT
        const payload = JSON.parse(atob(data.tokens.access.split(".")[1]));

        // Redirect based on role
        if (payload.role === "SUPER_ADMIN") {
            window.location.href = "/dashboard/super-admin/";
        } else {
            window.location.href = "/dashboard/admin/";
        }
    } catch (err) {
        document.getElementById("error").innerText = err.message;
    }
});
