/*
	Adds a favicon to the left of each link. Also quickly launches a website when a specific key is pressed.
*/

function setDefaultFavicon(image)
{
    image.onerror = '';
    image.src = 'favicons/default.ico';
    image.className = 'default-favicon';
    return true;
}

document.addEventListener("DOMContentLoaded", function()
{
	var links = document.getElementsByTagName('a');

	// add img tag before each anchor tag
	for (var i = 0; i < links.length; i++)
	{
		var favicon = links[i].href.split('/')[2] + '.ico'

		// load default.ico if no favicon found
		links[i].insertAdjacentHTML('beforebegin', '<img src="favicons/' + favicon +'" onerror="setDefaultFavicon(this);">');
	}

	// open certain website when specific key pressed 
	document.onkeypress = function(e)
	{
		if (e.key.toLowerCase() == 'g')
			window.location.href = 'https://google.com'
		else if (e.key.toLowerCase() == 'd')
			window.location.href = 'https://duckduckgo.com'
	};
});
