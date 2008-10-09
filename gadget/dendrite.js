
var VIEWER = "viewer";
var BASE_URL = "http://1.latest.xerblin.appspot.com";

var FETCH_TEXT = {};
FETCH_TEXT[gadgets.io.RequestParameters.CONTENT_TYPE] = 
           gadgets.io.ContentType.TEXT;
           

var STATUS = new gadgets.MiniMessage("dendrite");

           
function tell(el, message) {
    document.getElementById(el).innerHTML = message;
}

function loadCards(vid, display_name) {
    STATUS.createDismissibleMessage("Retrieving your cards...");
    var url = BASE_URL + "/cards";
    // Put in args, there must be a function for this already
    gadgets.io.makeRequest(
        url,
        function (data) {
            tell(STATUS, "Cards loaded.");
            tell("cards", data.text);
            gadgets.window.adjustHeight();
        },
        FETCH_TEXT
        );
    STATUS.createDismissibleMessage("Card request sent...");
}

function loadViewer() {
    STATUS.createDismissibleMessage("Loading your data...");
    var req = opensocial.newDataRequest();
// http://code.google.com/apis/opensocial/docs/0.7/reference/opensocial.DataRequest.html
    req.add(
// http://code.google.com/apis/opensocial/docs/0.7/reference/opensocial.DataRequest.html#newFetchPersonRequest
        req.newFetchPersonRequest(opensocial.IdSpec.PersonId.VIEWER),
        VIEWER
        );
    req.send(onLoadViewer);
    STATUS.createDismissibleMessage("Request for your data sent...");
}

function onLoadViewer(data) {
    STATUS.createDismissibleMessage("Your data request has returned.");
// http://code.google.com/apis/opensocial/docs/0.7/reference/opensocial.Person.html
    var viewer = data.get(VIEWER).getData();
    var display_name = viewer.getDisplayName();
    tell("user_display_name", "Hello " + display_name);
    loadCards(viewer.getId(), display_name);

//    var emails = viewer.getField(opensocial.Person.Field.EMAILS)
//    document.getElementById("email").innerHTML = emails;
//    var email = emails[0].getField(opensocial.Email.Field.ADDRESS);
//    document.getElementById("email").innerHTML = email;
}


function init() {
    loadViewer();
}

gadgets.util.registerOnLoadHandler(init);


