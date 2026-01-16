const API_BASE = "http://localhost:8000/api";
let editingCareerId = null;

function authHeaders() {
    return {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + localStorage.getItem("access_token"),
    };
}

function isBlockedAdmin() {
    const payload = JSON.parse(atob(localStorage.getItem("access_token").split(".")[1]));
    return payload.role === "ADMIN" && payload.can_access === false;
}

async function loadCareers() {
    const careers = await apiFetch(`${API_BASE}/careers/cms/`, {
        headers: authHeaders(),
    });

    const tbody = document.querySelector("#careersTable tbody");
    tbody.innerHTML = "";

    careers.forEach(c => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>
                <svg width="24" height="24" viewBox="0 0 24 24">
                    <path d="${c.svg_d_value || ''}"></path>
                </svg>
            </td>
            <td>${c.title}</td>
            <td>${c.one_line_desc}</td>
            <td>${new Date(c.updated_at).toLocaleString()}</td>
            <td>
                <button onclick="editCareer('${c.id}')">Edit</button>
                <button onclick="deleteCareer('${c.id}')">Delete</button>
            </td>
        `;

        if (isBlockedAdmin()) {
            tr.querySelectorAll("button").forEach(b => b.disabled = true);
        }

        tbody.appendChild(tr);
    });
}


function openCareerModal(career = null) {
    if (isBlockedAdmin()) return;

    document.getElementById("careerModal").classList.remove("hidden");
    document.getElementById("careerModalTitle").innerText =
        career ? "Edit Career" : "Add Career";

    editingCareerId = career ? career.id : null;

    ["title","one_line_desc","freshers_desc","experienced_desc","svg_d_value"]
        .forEach(id => document.getElementById(id).value = career ? career[id] || "" : "");

    updateSVGPreview();
}

function closeCareerModal() {
    document.getElementById("careerModal").classList.add("hidden");
}

document.getElementById("svg_d_value")?.addEventListener("input", updateSVGPreview);

function updateSVGPreview() {
    document.getElementById("svgPreviewPath").setAttribute(
        "d",
        document.getElementById("svg_d_value").value
    );
}

async function saveCareer() {
    const payload = {
        title: title.value,
        one_line_desc: one_line_desc.value,
        freshers_desc: freshers_desc.value,
        experienced_desc: experienced_desc.value,
        svg_d_value: svg_d_value.value,
    };

    const url = editingCareerId
        ? `${API_BASE}/careers/cms/${editingCareerId}/update/`
        : `${API_BASE}/careers/cms/create/`;

    const method = editingCareerId ? "PUT" : "POST";

    await apiFetch(url, {
        method,
        headers: authHeaders(),
        body: JSON.stringify(payload),
    });

    closeCareerModal();
    loadCareers();
}

async function editCareer(id) {
    const careers = await apiFetch(`${API_BASE}/careers/cms/`, {
        headers: authHeaders(),
    });

    const career = careers.find(c => c.id === id);
    openCareerModal(career);
}


async function deleteCareer(id) {
    if (isBlockedAdmin()) return;
    if (!confirm("Delete this career?")) return;

    await apiFetch(`${API_BASE}/careers/cms/${id}/delete/`, {
        method: "DELETE",
        headers: authHeaders(),
    });

    loadCareers();
}
