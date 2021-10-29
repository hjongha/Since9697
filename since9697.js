var memid = new Array();
memid[0] = "hjongha";

var mempass = new Array();
mempass[0] = "1234";

var check_id = 0;

function id_check(form)
{
	if (form.id.value=="") {
		alert("아이디를 입력해주세요.");
		return 0;
	}
	else if ((form.id.value).length < 6) {
		alert("형식에 맞게 입력해주세요.");
		return 0;
	}
	
	for(var i=0; i<memid.length; i++) {
		if (form.id.value==memid[i]) {
			alert("중복된 아이디 입니다.");
			return 0;
		}
	}
	alert("사용 가능한 아이디입니다.");
	check_id = 1;
}

function joinmem(form)
{
	if(check_id==1 && form.pw.value==form.pw_ch.value) {
		alert(form.id.value+"님, 회원가입을 환영합니다!");
		memid[memid.length] = form.id.value;
		mempass[mempass.length] = form.pw.value;
		window.open("since9697.html");
		window.close();
	}
	else if(check_id=0) {
		alert("아이디 중복을 확인해주세요.");
	}
	else if(!(form.pw.value==form.pw_ch.value)) {
		alert("비밀번호 확인이 다릅니다.");
	}
}

function check(form)
{
	for(var i=0; i<memid.length; i++) {
		if(form.userid.value==memid[i]) {
			if (form.userpass.value==mempass[i]) {
				alert("환영합니다");
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
