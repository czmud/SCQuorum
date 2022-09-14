let count = 0;
let searchText = document.getElementById('friend-search-input').value;
const user_id = document.getElementById('user-id-from-session').value;

function handleTextInput(event){
    searchText = event.target.value;
    count++;
    setTimeout(() => {
        count--;
        if( count > 0 ){
            return;
        }
        friendsSearch(searchText, user_id);
    }, 1000)
}

function searchButtonClick(event){
    event.preventDefault();
    friendsSearch(searchText, user_id);
}

function friendsSearch(searchText, user_id){
    searchText = searchText.trim();
    let element = document.getElementById('friend-search-results');
    if( searchText.length < 1 ){
        element.innerHTML = "";
        return;
    }
    let innerHTML = ""
    fetch('http://localhost:5000/api/friends/'+user_id+"/"+searchText )
        .then( response => response.json() )
        .then( data => {
            ( data.message.length > 0 ?
                data.message.map( friend => (
                    innerHTML += "<div class='d-flex justify-content-center align-items-center m-2'>"
                    +"<h3 class='mx-2'>"+friend.full_name+"</h3>"
                    +"<a class='btn btn-info mx-2' href='/send_friend_request/"+friend.id+"' role='button'>+Request</a>"
                    +"</div>"))
            :
            innerHTML += "<div class='rounded m-2'>"
            +"<h3>No users with that name were found</h3>"
            +"</div>"
        );
        element.innerHTML = innerHTML;
        })
}

friendsSearch( searchText, user_id );