// JavaScript Document

function popup(action)
{
	if (action == 1)
	{
		document.getElementById("popup").style.height = document.body.clientHeight + "px";
		document.getElementById("popup").style.display = "block";
		document.getElementById("popbox").style.display = "block";
	}
	else
	{
		document.getElementById("popup").style.display = "none";
		document.getElementById("popbox").style.display = "none";
	}
}