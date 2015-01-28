//$(function(){
//var search_text;
//
//    $('#hike_search').keyup(function(){
//        console.log("keyup is activated");
//        search_text = $('#hike_search').val();
//        console.log(search_text);
//        $('#search-results').html('&nbsp;').load('/search/?search_text=' + search_text);
////        $.ajax({
////           type: "POST",
////           url: "/search/",
////           data: search_text,
////           success: searchSuccess,
////           dataType: 'html'
////        });
//
//    });
//
//});
//
//function searchSuccess(data, textStatus, jqXHR)
//{
//    $('#search-results').html(data);
//}

(function() {
    var ajaxRequest;

    function initSearch() {
        console.log('init search');
        // set up AJAX request
        ajaxRequest = getXmlHttpObject();
        if (ajaxRequest == null) {
            alert("This browser does not support HTTP Request");
            return;
        }
        var searchField = document.getElementById("hike_search");
        searchField.onkeyup = function () {
            searchRequest(searchField)
        };

    }

    function getXmlHttpObject() {
        if (window.XMLHttpRequest) {
            return new XMLHttpRequest();
        }
        if (window.ActiveXObject) {
            return new ActiveXObject("Microsoft.XMLHTTP");
        }
        return null;
    }

    function searchRequest(searchField) {
//    console.log('keyup');
//    console.log(searchField);
        var search_text = searchField.value;
//    console.log(search_text);
        var search = '/search/?search_text=' + encodeURI(search_text);
        ajaxRequest.open('GET', search, true);
        ajaxRequest.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        ajaxRequest.send(search_text);
        ajaxRequest.onreadystatechange = stateChanged;
    }

    function stateChanged() {
        if (ajaxRequest.readyState == 4) {
            //use the info here that was returned
            if (ajaxRequest.status == 200) {
                var data = JSON.parse(ajaxRequest.responseText);
                searchResults(data);

            }
        }
    }

    function searchResults(data){
        var results,
            url,
            name,
            distance,
            difficulty,
            text;
        var output = [];
        results = document.getElementById("search-results");
        for(i=0; i<data.length; i++) {
            url = "/hikes/hike/" + data[i].hikeUrl;
            name = data[i].hike;
            distance = " | Length: " + data[i].distance;
            difficulty = " miles | Difficulty: " + data[i].difficulty;
            text = '<a href="' + url + '">'
                + name + '</a> ' + distance + difficulty;
            output.push(text);
        }
        console.log(ajaxRequest.responseText);
        results.innerHTML = "<li>" + output.join("</li><li>") + "</li>";

    }

    initSearch();
})();

//
//set header
