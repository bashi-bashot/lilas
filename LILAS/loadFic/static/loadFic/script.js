
// Script LoadFic index.html

var upload = document.getElementsByTagName("INPUT")[12];   //desactivation du bouton "valider" au lancement de la page
upload.disabled = true;                                    //pour me visualiser l'element input dans la liste, faire : console.log(document.getElementsByTagName("INPUT"))

// var element = document.getElementsByClassName("errorfile");  //recherche l'existance d'un élément "errorfile"
// //If it isn't "undefined" and it isn't "null", then it exists.
// for (var i=0; i<element.length; i++) {               
//     if(typeof(element[i]) != 'undefined' && element[i] != null){
//         // document.getElementById('myForm').reset();
//         // location.reload(true);
//         location.replace('loadFic');
//     }
// }

var formFilled = setInterval(function() {
    var valFileConf = document.getElementById('id_fileConf').value;
    var valFileSyst = document.getElementById('id_fileSyst').value;
    var valFileOpe = document.getElementById('id_fileOpe').value;
    var valFileCom = document.getElementById('id_fileCom').value;
    var valFileInc = document.getElementById('id_fileInc').value;

    if (valFileConf=="" && valFileSyst=="" && valFileOpe=="" && valFileCom=="" && valFileInc=="") {
        var elmt = document.getElementsByTagName("INPUT")[12];   //desactivation du bouton "valider" tant qu'aucun champ n'est rempli
        elmt.disabled = true;
    
    } else {
        var elmt = document.getElementsByTagName("INPUT")[12];   //activation du bouton "valider" lorsqu'un champ est rempli
        elmt.disabled = false;
        

        //----- Activation d.u.es bouton.s reset symbolise.s par une croix -----//
        if (valFileConf!="") {
            var button = document.getElementById('resetConf');
            button.style.visibility = "visible";
            
        };

        if (valFileSyst!="") {
            var button = document.getElementById('resetSyst');
            button.style.visibility = "visible";
        };

        if (valFileOpe!="") {
            var button = document.getElementById('resetOpe');
            button.style.visibility = "visible";
        };

        if (valFileCom!="") {
            var button = document.getElementById('resetCom');
            button.style.visibility = "visible";
        };
    
        if (valFileInc!="") {
            var button = document.getElementById('resetInc');
            button.style.visibility = "visible";
        };
        //----- Fin Activation d.u.es bouton.s reset symbolise.s par une croix -----//
    };
}, 100); //test effectue toutes les 100ms


//----- Suppresion d.u.es fichier.s selectionne.s -----//
document.getElementById("resetConf").addEventListener("click", myResetConf);
function myResetConf() {
    document.getElementById('id_fileConf').value="";
    var button = document.getElementById('resetConf');
    button.style.visibility = "hidden";
};

document.getElementById("resetSyst").addEventListener("click", myResetSyst);
function myResetSyst() {
    document.getElementById('id_fileSyst').value="";
    var button = document.getElementById('resetSyst');
    button.style.visibility = "hidden";
};

document.getElementById("resetOpe").addEventListener("click", myResetOpe);
function myResetOpe() {
    document.getElementById('id_fileOpe').value="";
    var button = document.getElementById('resetOpe');
    button.style.visibility = "hidden";
};

document.getElementById("resetCom").addEventListener("click", myResetCom);
function myResetCom() {
    document.getElementById('id_fileCom').value="";
    var button = document.getElementById('resetCom');
    button.style.visibility = "hidden";
};

document.getElementById("resetInc").addEventListener("click", myResetInc);
function myResetInc() {
    document.getElementById('id_fileInc').value="";
    var button = document.getElementById('resetInc');
    button.style.visibility = "hidden";
};
//----- Fin Suppresion d.u.es fichier.s selectionne.s -----//


document.getElementsByTagName("INPUT")[12].addEventListener("click", myUpload);
function myUpload() {

    clearInterval(formFilled);      //arret du test sur le remplissage du formulaire

    var bodyParent = document.getElementsByTagName("p")[1];     //visualisation du televersement via un spinner en mouvement
    bodyParent.innerHTML = "<p><div id='loader'></div>Upload in Progress</p>";

    var elmt = document.getElementsByTagName('html')[0];    //visualisation du televersement via un curseur souris en mouvement
    elmt.style.cursor = "wait";

    elmt = document.getElementById('adminPanel');       //desactivation du bouton "Panneaux d'administration" pdt le televersement
    elmt.style.cursor = "wait";
    elmt.disabled = true;

    elmt = document.getElementsByClassName('boutonApp');       //desactivation des bouton "Application" pdt le televersement
    for (var i=0; i<elmt.length; i++) {               
        elmt[i].style.cursor = "wait";
        elmt[i].onclick = function() { alert("Veuillez attendre la fin du telechargement.."); };                
    }
    //----- suppression d.u.es bouton.s "reset" pdt le televersement -----//
    var button = document.getElementById('resetConf');
    button.style.visibility = "hidden";
    var button = document.getElementById('resetSyst');
    button.style.visibility = "hidden";
    var button = document.getElementById('resetOpe');
    button.style.visibility = "hidden";
    var button = document.getElementById('resetCom');
    button.style.visibility = "hidden";
    var button = document.getElementById('resetInc');
    button.style.visibility = "hidden";
    //----- Fin suppression d.u.es bouton.s "reset" pdt le televersement -----//

    setTimeout(function(){  //desactivation des formulaires pdt le televersement
        
        elmt = document.getElementsByTagName("INPUT")[12];       //desactivation du bouton "valider" pdt le televersement
        elmt.style.cursor = "wait";
        elmt.disabled = true;

        elmt = document.getElementById('id_fileConf');
        elmt.style.cursor = "wait";
        elmt.disabled = true;
        elmt = document.getElementById('id_fileSyst');
        elmt.style.cursor = "wait";
        elmt.disabled = true;
        elmt = document.getElementById('id_fileOpe');
        elmt.style.cursor = "wait";
        elmt.disabled = true;
        elmt = document.getElementById('id_fileCom');
        elmt.style.cursor = "wait";
        elmt.disabled = true;
        elmt = document.getElementById('id_fileInc');
        elmt.style.cursor = "wait";
        elmt.disabled = true;
        
    }, 100);  //100ms necessaires afin de laisser le temps au server de lancer le televersement
    setTimeout(function() { alert("[ ATTENTION ]\n\nNe pas actualiser cette page web lors du téléversement des fichiers."); }, 1);

};
