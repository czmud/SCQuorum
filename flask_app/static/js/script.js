


function showHideNote(){
    let noteElement = document.getElementById("note-form")
    if (noteElement.style.visibility === "hidden"){
        noteElement.style.visibility = "visible";
        console.log(noteElement)
        document.getElementById("note-button-draft").style.display = "none";
    } else {
        noteElement.style.visibility = "hidden";
        let fieldElements = document.querySelectorAll(".note-input");
        for ( let field of fieldElements ) {
            field.value = "";
        }
        document.getElementById("note-button-draft").style.display = ""
    }
}