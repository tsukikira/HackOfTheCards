$.ajaxSetup ({
	cache: false
});

function populateChat() {
	var url = "/chat";
	$("#ChatHistory").load(url);
}

setInterval(populateChat, 1000);
