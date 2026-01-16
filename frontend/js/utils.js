function renderNavbar(role) {
    const nav = document.getElementById("navbar");

    let links = [];

    if (role === "SUPER_ADMIN") {
        links = [
            { label: "Admins", href: "/admins/" },
            { label: "Careers", href: "/careers/" },
            { label: "Products", href: "#" },
            { label: "Services", href: "#" },
        ];
    } else {
        links = [
            { label: "Careers", href: "/careers/" },
            { label: "Products", href: "#" },
            { label: "Services", href: "#" },
        ];
    }

    nav.innerHTML = `
        <div class="nav-left">
            <strong>CMS</strong>
        </div>
        <div class="nav-right">
            ${links.map(l => `<a href="${l.href}">${l.label}</a>`).join("")}
            <button onclick="logout()">Logout</button>
        </div>
    `;
}

function logout() {
    localStorage.clear();
    window.location.href = "/login/";
}

function showToast(message, type = "success") {
    const toast = document.getElementById("toast");
    if (!toast) return;

    toast.innerText = message;
    toast.className = `toast ${type}`;
    toast.classList.remove("hidden");

    setTimeout(() => {
        toast.classList.add("hidden");
    }, 3000);
}

function showLoader() {
    document.getElementById("loader")?.classList.remove("hidden");
}

function hideLoader() {
    document.getElementById("loader")?.classList.add("hidden");
}

async function apiFetch(url, options = {}) {
    showLoader();

    const headers = options.headers || {};
    headers["Content-Type"] = "application/json";

    const token = localStorage.getItem("access_token");
    if (token) {
        headers["Authorization"] = "Bearer " + token;
    }

    try {
        const res = await fetch(url, {
            ...options,
            headers,
        });

        const data = await res.json().catch(() => ({}));

        if (!res.ok) {
            throw new Error(data.detail || "Something went wrong");
        }

        return data;
    } catch (err) {
        showToast(err.message, "error");
        throw err;
    } finally {
        hideLoader();
    }
}
