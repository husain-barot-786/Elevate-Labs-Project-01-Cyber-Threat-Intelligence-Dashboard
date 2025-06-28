let socket = io();
let username = "";
let userKeyPair = null;
let publicKeys = {};
let aesKeys = {};
let currentRecipient = "";
let onlineUsers = [];
let groups = {};
let groupKeys = {};

// UI FEEDBACK
function showError(msg) {
    let e = document.getElementById("error-message");
    e.innerText = msg;
    e.style.display = "block";
    setTimeout(()=>{ e.style.display="none"; }, 3500);
}
function showSuccess(msg) {
    let e = document.getElementById("success-message");
    e.innerText = msg;
    e.style.display = "block";
    setTimeout(()=>{ e.style.display="none"; }, 2500);
}

// Register function made globally accessible
async function register() {
    username = document.getElementById("username").value.trim();
    if (!username) return showError("Enter username!");
    try {
        userKeyPair = await generateKeyPair();
    } catch(err) {
        showError("Browser does not support crypto: "+err);
        return;
    }
    document.getElementById("login").style.display = "none";
    document.getElementById("chat").style.display = "";
    let curUserSpan = document.getElementById("current-user");
    if (curUserSpan) curUserSpan.innerText = username;
    socket.emit("register", {
        username,
        publicKey: userKeyPair.publicKey
    });
}
window.register = register;

// User online/offline
socket.on("user_status", function({online, all_users}) {
    onlineUsers = online;
    updateUserList(all_users, online);
    updateRecipientOptions();
});

// When you get the list of public keys, establish session with each peer
socket.on("public_keys", async function(allPublicKeys) {
    publicKeys = allPublicKeys;
    delete publicKeys[username];
    updateRecipientOptions();
    for (let peer of Object.keys(publicKeys)) {
        if (!aesKeys[peer]) {
            let aesKey = window.crypto.getRandomValues(new Uint8Array(32));
            aesKeys[peer] = aesKey;
            let encAesKey = await encryptWithPublicKey(publicKeys[peer], aesKey);
            socket.emit("send_message", {
                sender: username,
                recipient: peer,
                ciphertext: "KEY:" + encAesKey
            });
        }
    }
});

// Group support
document.getElementById("group-create-btn").onclick = () => {
    document.getElementById("group-modal").style.display = "";
    document.getElementById("group-name-input").value = "";
    let list = document.getElementById("group-users-list");
    list.innerHTML = "";
    for(let u of Object.keys(publicKeys)) {
        let cb = document.createElement("input");
        cb.type = "checkbox";
        cb.value = u;
        cb.className = "group-user-checkbox";
        let label = document.createElement("label");
        label.innerText = u;
        label.prepend(cb);
        list.appendChild(label);
        list.appendChild(document.createElement("br"));
    }
};
document.getElementById("close-modal").onclick = () => {
    document.getElementById("group-modal").style.display = "none";
};
document.getElementById("create-group-btn").onclick = async () => {
    let groupName = document.getElementById("group-name-input").value.trim();
    if(!groupName) return showError("Group name required!");
    let checked = Array.from(document.querySelectorAll(".group-user-checkbox:checked")).map(cb=>cb.value);
    if(checked.length<1) return showError("Select at least 1 user!");
    checked.push(username);
    let groupKey = window.crypto.getRandomValues(new Uint8Array(32));
    groupKeys[groupName] = groupKey;
    groups[groupName] = {members:checked, groupKey, isMine:true};
    socket.emit("create_group", {
        group: groupName,
        members: checked
    });
    for(let u of checked) {
        if(u===username) continue;
        let encKey = await encryptWithPublicKey(publicKeys[u], groupKey);
        socket.emit("send_group_key", {group: groupName, to: u, encKey});
    }
    showSuccess("Group created!");
    document.getElementById("group-modal").style.display = "none";
    updateRecipientOptions();
};
socket.on("receive_group_key", async ({group, encKey, from})=>{
    let groupKey = await decryptWithPrivateKey(userKeyPair.privateKey, encKey);
    groupKeys[group] = groupKey;
    groups[group] = groups[group] || {};
    groups[group].groupKey = groupKey;
    showSuccess(`Added to group "${group}" by ${from}`);
    updateRecipientOptions();
});
socket.on("group_created", ({group, members})=>{
    groups[group] = groups[group] || {};
    groups[group].members = members;
    updateRecipientOptions();
});

// Recipients dropdown: only online users and groups available
function updateRecipientOptions() {
    let sel = document.getElementById("recipients");
    let last = sel.value;
    sel.innerHTML = "";
    for(let g of Object.keys(groups)) {
        let opt = document.createElement("option");
        opt.value = "group:"+g;
        opt.innerText = "👥 "+g;
        opt.className = "group-option";
        sel.appendChild(opt);
    }
    for(let u of onlineUsers) {
        if(u !== username) {
            let opt = document.createElement("option");
            opt.value = u;
            opt.innerText = u;
            sel.appendChild(opt);
        }
    }
    if(last && Array.from(sel.options).some(o=>o.value===last))
        sel.value = last;
    else if(sel.options.length>0)
        sel.value = sel.options[0].value;
    currentRecipient = sel.value;
    sel.onchange = () => currentRecipient = sel.value;
}

// User list (sidebar): only online users, except yourself
function updateUserList(all, online) {
    let ul = document.getElementById("user-list");
    ul.innerHTML = "<strong>Users</strong>";
    for(let u of online) {
        if(u===username) continue;
        let div = document.createElement("div");
        div.className = "user-status";
        div.appendChild(document.createTextNode(u));
        ul.appendChild(div);
    }
}

// Send message with E2EE (group/individual)
async function sendMessage() {
    let recipient = document.getElementById("recipients").value;
    let plaintext = document.getElementById("messageInput").value;
    if (!plaintext) return;
    if(recipient.startsWith("group:")) {
        let group = recipient.slice(6);
        let aesKey = groupKeys[group];
        if(!aesKey) return showError("No group key! Wait for group setup.");
        let iv = window.crypto.getRandomValues(new Uint8Array(16));
        let ciphertext = await encryptAES(aesKey, iv, plaintext);
        socket.emit("send_group_message", {
            group,
            sender: username,
            ciphertext: "MSG:" + arrayBufferToBase64(iv) + ":" + arrayBufferToBase64(ciphertext)
        });
        // Only display once for the sender
        addMessage(username, `[${group}] ${plaintext}`, true);
    } else {
        let aesKey = aesKeys[recipient];
        if (!aesKey) {
            aesKey = window.crypto.getRandomValues(new Uint8Array(32));
            aesKeys[recipient] = aesKey;
            let encAesKey = await encryptWithPublicKey(publicKeys[recipient], aesKey);
            socket.emit("send_message", {
                sender: username,
                recipient,
                ciphertext: "KEY:" + encAesKey
            });
        }
        let iv = window.crypto.getRandomValues(new Uint8Array(16));
        let ciphertext = await encryptAES(aesKey, iv, plaintext);
        socket.emit("send_message", {
            sender: username,
            recipient,
            ciphertext: "MSG:" + arrayBufferToBase64(iv) + ":" + arrayBufferToBase64(ciphertext)
        });
        addMessage(username, plaintext, true);
    }
    document.getElementById("messageInput").value = "";
}
window.sendMessage = sendMessage;

// Receive messages from server
socket.on("receive_message", async function(data) {
    let sender = data.sender;
    let recipient = data.recipient;
    let ciphertext = data.ciphertext;
    if (recipient !== username && !(ciphertext.startsWith("KEY:") && sender in publicKeys)) {
        return;
    }
    if (ciphertext.startsWith("KEY:")) {
        let encAesKey = ciphertext.slice(4);
        let aesKey = await decryptWithPrivateKey(userKeyPair.privateKey, encAesKey);
        aesKeys[sender] = aesKey;
        addInfoMessage(`[Secure channel established with ${sender}]`);
    } else if (ciphertext.startsWith("MSG:")) {
        let [_, ivB64, ctB64] = ciphertext.split(":");
        let aesKey = aesKeys[sender];
        if (!aesKey) {
            aesKey = window.crypto.getRandomValues(new Uint8Array(32));
            aesKeys[sender] = aesKey;
            let encAesKey = await encryptWithPublicKey(publicKeys[sender], aesKey);
            socket.emit("send_message", {
                sender: username,
                recipient: sender,
                ciphertext: "KEY:" + encAesKey
            });
            addInfoMessage(`[Cannot decrypt: No session key from ${sender}]`);
            return;
        }
        let iv = base64ToArrayBuffer(ivB64);
        let ct = base64ToArrayBuffer(ctB64);
        let plaintext = await decryptAES(aesKey, iv, ct);
        if (sender !== username) {
            addMessage(sender, plaintext, false);
        }
    }
});

// Group message receive
socket.on("receive_group_message", async function({group, sender, ciphertext}){
    if(!groupKeys[group]) return;
    if(ciphertext.startsWith("MSG:")) {
        let [_, ivB64, ctB64] = ciphertext.split(":");
        let iv = base64ToArrayBuffer(ivB64);
        let ct = base64ToArrayBuffer(ctB64);
        let plaintext = await decryptAES(groupKeys[group], iv, ct);
        // Only display group message if NOT from self
        if(sender !== username) {
            addMessage(sender, `[${group}] ${plaintext}`, false);
        }
    }
});

// Info and chat bubbles
function addMessage(sender, text, isSelf) {
    let msgs = document.getElementById("messages");
    let div = document.createElement("div");
    div.className = "msg-bubble " + (isSelf ? "msg-self" : "msg-peer");
    div.innerHTML = `<strong>${isSelf ? "You" : escapeHTML(sender)}:</strong> ${escapeHTML(text)}`;
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
}
function addInfoMessage(text) {
    let msgs = document.getElementById("messages");
    let div = document.createElement("div");
    div.className = "msg-bubble msg-info";
    div.innerText = text;
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
}
function escapeHTML(str) {
    if(!str) return '';
    return str.replace(/[<>&"']/g, function(c) {
        return ({
            '<': '&lt;',
            '>': '&gt;',
            '&': '&amp;',
            '"': '&quot;',
            "'": '&#39;'
        })[c];
    });
}

// Crypto
async function generateKeyPair() {
    let key = await window.crypto.subtle.generateKey(
        {name: "RSA-OAEP", modulusLength: 2048, publicExponent: new Uint8Array([1,0,1]), hash: "SHA-256"},
        true,
        ["encrypt", "decrypt"]
    );
    let publicKeyPem = await exportPublicKey(key.publicKey);
    return {publicKey: publicKeyPem, privateKey: key.privateKey};
}
async function exportPublicKey(key) {
    let spki = await window.crypto.subtle.exportKey("spki", key);
    let b64 = arrayBufferToBase64(spki);
    let pem = "-----BEGIN PUBLIC KEY-----\n";
    for (let i = 0; i < b64.length; i += 64) pem += b64.substring(i, i+64) + "\n";
    pem += "-----END PUBLIC KEY-----";
    return btoa(pem);
}
async function encryptWithPublicKey(peerPemB64, aesKey) {
    let pem = atob(peerPemB64);
    let b64 = pem.replace(/-----(BEGIN|END) PUBLIC KEY-----|\n/g, '');
    let spki = base64ToArrayBuffer(b64);
    let peerKey = await window.crypto.subtle.importKey(
        "spki", spki, {name: "RSA-OAEP", hash: "SHA-256"}, false, ["encrypt"]
    );
    let enc = await window.crypto.subtle.encrypt({name: "RSA-OAEP"}, peerKey, aesKey);
    return arrayBufferToBase64(enc);
}
async function decryptWithPrivateKey(privateKey, encAesKeyB64) {
    let enc = base64ToArrayBuffer(encAesKeyB64);
    let aesKey = await window.crypto.subtle.decrypt({name: "RSA-OAEP"}, privateKey, enc);
    return new Uint8Array(aesKey);
}
async function encryptAES(aesKey, iv, plaintext) {
    let key = await window.crypto.subtle.importKey(
        "raw", aesKey, {name: "AES-CBC"}, false, ["encrypt"]
    );
    let enc = await window.crypto.subtle.encrypt(
        {name: "AES-CBC", iv: iv}, key,
        new TextEncoder().encode(plaintext)
    );
    return new Uint8Array(enc);
}
async function decryptAES(aesKey, iv, ciphertext) {
    let key = await window.crypto.subtle.importKey(
        "raw", aesKey, {name: "AES-CBC"}, false, ["decrypt"]
    );
    let dec = await window.crypto.subtle.decrypt(
        {name: "AES-CBC", iv: iv}, key, ciphertext
    );
    return new TextDecoder().decode(dec);
}
function arrayBufferToBase64(ab) {
    return btoa(String.fromCharCode(...new Uint8Array(ab)));
}
function base64ToArrayBuffer(b64) {
    let binary = atob(b64);
    let bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
    return bytes.buffer;
}
function logout() {
    location.reload();
}
window.logout = logout;