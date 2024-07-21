
function getCookieValue(name) {
    const re = new RegExp(name + '=([^;]+)');
    const value = re.exec(document.cookie);
    return (value != null) ? unescape(value[1]) : null;
}

function setCookieValue(key, value, days) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = key + '=' + encodeURIComponent(value) + ';expires=' + expires + ';path=/';
}

function fallback() {
    if (window.location.pathname === '/fallback') {
        return;
    }
    let msg = 'Please login to continue.';
    window.location.href = '/fallback?msg=' + encodeURIComponent(msg);
}

function loginTgWebApp() {
    let tg = window.Telegram.WebApp;
    if (!tg.initDataUnsafe.user) {
        fallback();
    }
    // Cookies.set('tg_user_id', tg.initDataUnsafe.user.id);
    setCookieValue('tg_user_id', tg.initDataUnsafe.user.id, 1);
}

function checkLogin() {
    return getCookieValue('tg_user_id')
}

// if (!Cookies.get('tg_user_id')) {
if (!checkLogin()) {
    loginTgWebApp();
}
