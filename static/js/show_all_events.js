let data;
let a;

$(document).ready(function() {
    a = 0;
    createPage()
});

function createPage() {
    a = 1;
    $.when(
        loadEvents()
    ).then(function() {
        initAll();
    });

    a = 4
}

function loadEvents() {
    let deff = $.Deffered()
    a = 2;
    $.ajax({
        url:  "http://localhost:5000/events/all",
        dataType: "json",
        success: function(result) {
            a = 5;
            events = result;
            deff.resolve();
        },
        error: function() {
            events = [];
            deff.resolve();
        }
    });

    a = 3;
    return deff.promise();
}

function initAll() {
    a = 6;
    $("#allEvents").text("Event: " + JSON.stringify(events))
}