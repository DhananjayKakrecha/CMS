function getToken() {
    return localStorage.getItem("access_token");
}

function decodeJWT(token) {
    try {
        const payload = token.split(".")[1];
        return JSON.parse(atob(payload));
    } catch {
        return null;
    }
}

function requireAuth() {
    const token = getToken();
    if (!token) {
        window.location.href = "/login/";
        return;
    }

    const payload = decodeJWT(token);
    if (!payload) {
        localStorage.clear();
        window.location.href = "/login/";
    }
}

function requireRole(role) {
    const token = getToken();
    const payload = decodeJWT(token);

    if (!payload || payload.role !== role) {
        window.location.href = "/login/";
    }
}

function isCMSBlocked() {
    const payload = decodeJWT(getToken());
    return payload && payload.role === "ADMIN" && payload.can_access === false;
}

function isTokenExpired(token) {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.exp * 1000 < Date.now();
}

(function enforceTokenValidity() {
    const token = localStorage.getItem("access_token");
    if (token && isTokenExpired(token)) {
        localStorage.clear();
        window.location.href = "/login/";
    }
})();
