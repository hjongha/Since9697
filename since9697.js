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
		if (document.writeln(form.passward == member[i].passward)) {
				return 1;
			}
			else {
				alert("아이디와 비밀번호를 확인해주세요.");
				return 0;
			}
		}
	}
	alert("아이디와 비밀번호를 확인해주세요.");
}
