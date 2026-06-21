function copiarTexto(id) {
    var el = document.getElementById(id);
    if (!el) { return; }
    el.select();
    el.setSelectionRange(0, 999999);
    navigator.clipboard.writeText(el.value).then(function () {
        alert("Copiado. Cole manualmente na IA, revise e envie voce mesmo.");
    }).catch(function () {
        document.execCommand("copy");
        alert("Copiado (modo compatibilidade). Cole manualmente na IA, revise e envie voce mesmo.");
    });
}
