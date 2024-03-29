function getSearchPhrase() {
    var message = document.getElementById('search_input').value;
    window.alert(message);
}

function openPage(pageName) {
    window.location.href = 'Pages/' + pageName;
}
