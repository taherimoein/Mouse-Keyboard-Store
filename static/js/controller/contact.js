

check_fields = function (thisuser_name, thisuser_email, thisuser_mobile, thisuser_message) {
    if ((thisuser_name.length != 0) & ((thisuser_mobile.length != 0 && thisuser_mobile.length == 11) | (thisuser_email.length != 0)) & (thisuser_message.length != 0)){
        return true;
    }else{
        return false;
    }
}
