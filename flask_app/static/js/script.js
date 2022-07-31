



// document.addEventListener("DOMContentLoaded", function() {
//     console.log(5)
//     highlightReferencedText("efficiency-improving measure");
// });

function highlightReferencedText(){
    searchText = document.getElementById("hacky-string-holder").innerHTML
    if (searchText === ""){
        return undefined
    }

    summaryText = document.getElementById("opinion-text").innerHTML;
    
    //text curation
    modifiedSearchText = searchText.replace(/[\u0028\u0029]/g, "Z")
    modifiedSummaryText = summaryText.replace(/[\u0028\u0029]/g, "Z")
    
    index = modifiedSummaryText.search(modifiedSearchText);
    if (index === -1){
        console.log("text not found")
    } else {
        document.getElementById("opinion-text").innerHTML = summaryText.slice(0,index) + "<span style='background-color: yellow'>" + searchText + "</span>" + summaryText.slice(index + searchText.length, summaryText.length);
        console.log("text replace")
    }

    console.log("finished")
}




function showHideNote(){
    let noteElement = document.getElementById("note-form")
    if (noteElement.style.visibility === "hidden"){
        noteElement.style.visibility = "visible";
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


highlightReferencedText();