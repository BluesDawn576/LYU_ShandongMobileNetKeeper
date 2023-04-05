let console_panel;
let consoleElement = document.getElementById('console');

eel.expose(log);
eel.expose(alert);
eel.expose(close_console_panel);
eel.expose(redirect_window);

function init() {
    get_account_info();
    console_panel = new mdui.Dialog("#running", {
        modal: true
    });
}

async function get_account_info() {
    let content = await eel.get_accinfo()();
    if (content !== null) {
        document.getElementById('acc').value = content[0];
        document.getElementById('pwd').value = content[1];
        mdui.updateTextFields();
    }
}

function about() {
    alert("本程序仅用于登录 NetKeeper 校园网。\n" +
        "写这个程序是因为自带的登录页面太难用，甚至有概率不会自动弹出。\n" +
        "走的是官方的api，每个地区不一定适用。\n\n" +
        "项目地址：" + "<a href=" + "https://github.com/BluesDawn576/LYU_ShandongMobileNetKeeper" + " target='_blank' class='anchor'>" + "BluesDawn576/LYU_ShandongMobileNetKeeper" + "</a>\n" +
        "由 python + eel + mdui 驱动", "这是什么")
}

function login() {
    let u = document.getElementById('acc').value;
    let p = document.getElementById('pwd').value;
    if (u === "" || p === "") {
        alert("请输入账号或密码", "提示");
    } else {
        eel.set_accinfo(u, p);
        eel.login(u, p);
        mdui.snackbar("正在登录，请稍等...", {
            timeout: 3000,
            closeOnOutsideClick: false
        });
    }
}

function scroll_to_bottom() {
 const domWrapper = document.querySelector('.console-text');
 (function smooth_scroll() {
     const currentScroll = domWrapper.scrollTop;
     const clientHeight = domWrapper.offsetHeight;
     const scrollHeight = domWrapper.scrollHeight;
     if (scrollHeight - 10 > currentScroll + clientHeight) {
         window.requestAnimationFrame(smooth_scroll);
         domWrapper.scrollTo(0, currentScroll + (scrollHeight - currentScroll - clientHeight) / 2);
    }
 })();
}

function log(text) {
    if (console_panel !== null) {
        if (console_panel.getState() === "closed") {
            console_panel.open();
            consoleElement.innerText = null;
        }
        consoleElement.innerText += text + '\n';
    }
    scroll_to_bottom();
}

function alert(text, title,) {
    text = text.replace(/\n/g,'<br>');
    mdui.alert(text, title);
}

function close_console_panel() {
    console_panel.close();
}

function redirect_window() {
    window.location.replace("success.html");
}