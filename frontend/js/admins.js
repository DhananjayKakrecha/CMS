const API_BASE = "http://localhost:8000/api";
let editingAdminId = null;

function authHeaders() {
    return {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + localStorage.getItem("access_token"),
    };
}

async function loadAdmins() {
    const admins = await apiFetch(`${API_BASE}/users/admins/`, {
        headers: authHeaders(),
    });

    const tbody = document.querySelector("#adminsTable tbody");
    tbody.innerHTML = "";

    admins.forEach(admin => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${admin.full_name}</td>
            <td>${admin.email}</td>
            <td>${admin.phone_no}</td>
            <td>
                <button onclick="toggleAccess('${admin.id}')">
                    ${admin.can_access ? "Enabled" : "Disabled"}
                </button>
            </td>
            <td>
                <button onclick="editAdmin('${admin.id}')">Edit</button>
                <button onclick="deleteAdmin('${admin.id}')">Delete</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}


function openAdminModal(admin = null) {
    document.getElementById("adminModal").classList.remove("hidden");
    document.getElementById("modalTitle").innerText = admin ? "Edit Admin" : "Add Admin";

    if (admin) {
        editingAdminId = admin.id;
        document.getElementById("full_name").value = admin.full_name;
        document.getElementById("email").value = admin.email;
        document.getElementById("phone_no").value = admin.phone_no;
        document.getElementById("address").value = admin.address;
        document.getElementById("password").value = "";
    } else {
        editingAdminId = null;
        ["full_name","email","phone_no","password","address"]
            .forEach(id => document.getElementById(id).value = "");
    }
}

function closeAdminModal() {
    document.getElementById("adminModal").classList.add("hidden");
}

async function saveAdmin() {
    const payload = {
        full_name: full_name.value,
        email: email.value,
        phone_no: phone_no.value,
        address: address.value,
    };

    // 🔥 only include password if provided
    if (password.value.trim()) {
        payload.password = password.value;
    }

    const url = editingAdminId
        ? `${API_BASE}/users/admins/${editingAdminId}/update/`
        : `${API_BASE}/users/admins/create/`;

    const method = editingAdminId ? "PUT" : "POST";

    await apiFetch(url, {
        method,
        headers: authHeaders(),
        body: JSON.stringify(payload),
    });

    closeAdminModal();
    loadAdmins();
}


async function editAdmin(id) {
    const admins = await apiFetch(`${API_BASE}/users/admins/`, {
        headers: authHeaders(),
    });

    const admin = admins.find(a => a.id === id);
    openAdminModal(admin);
}


async function deleteAdmin(id) {
    if (!confirm("Delete this admin?")) return;

    await apiFetch(`${API_BASE}/users/admins/${id}/delete/`, {
        method: "DELETE",
        headers: authHeaders(),
    });

    loadAdmins();
}

async function toggleAccess(id) {
    await apiFetch(`${API_BASE}/users/admins/${id}/toggle-access/`, {
        method: "PATCH",
        headers: authHeaders(),
    });

    loadAdmins();
}

