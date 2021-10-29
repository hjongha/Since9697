function member() {
	var id;
	var passward;
	var name;
	var phonenum;
}

var member = new Array();

function plusmember(form) 
{
	member[member.length].id = form.id;
	member[member.length].passward = form.passward;
	member[member.length].name = form.name;
	member[member.length].phonenum = form.phonenum;
}

function check(form)
{
	for(var i=0; i<member.length; i++) {
		if(document.writeln(form.id == member[i].id)
			return 1;
	}
	return 0;
}
